from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from . import main
from app.models import Adopter
from app.forms import UserForm, LoginForm
from app import db


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/adopter_register', methods=['GET', 'POST'])
def adopter_register():
    form = UserForm()
    if form.validate_on_submit():

        if form.name.data:
            user_name = Adopter.query.filter_by(
                name=form.name.data).first()
            if user_name:
                flash('该用户名已注册，请重新填写用户名')
                return render_template('adopter_register.html', form=form)
        if form.mobile.data:
            user_mobile = Adopter.query.filter_by(
                mobile=form.mobile.data).first()
            if user_mobile:
                flash('该手机号已注册，请重新填写手机号')
                return render_template('adopter_register.html', form=form)
        new_register = Adopter()
        form.populate_obj(new_register)
        new_register.pwd = form.password.data
        db.session.add(new_register)
        try:
            db.session.commit()
            flash('注册成功')
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请重试')
        return redirect(url_for('main.login'))
    return render_template(
        'adopter_register.html',
        form=form,
    )


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.mobile.data:
            adopter_user = Adopter.query.filter_by(
                mobile=form.mobile.data
            ).first()
            if adopter_user is not None and adopter_user.verify_pwd(form.password.data):
                login_user(adopter_user)
                return redirect(url_for(request.args.get('next') or 'main.index'))
            flash('错误的手机号或者密码')
    return render_template(
        'login.html',
        form=form
    )


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('成功退出')
    return redirect(url_for('main.index'))