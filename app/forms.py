from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField('请输入用户名', validators=[DataRequired()])
    mobile = StringField('请输入手机号', validators=[DataRequired()])
    password = PasswordField('请输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    mobile = StringField('请输入手机号', validators=[DataRequired()])
    password = PasswordField('请输入密码', validators=[DataRequired()])
    submit = SubmitField('Submit')
