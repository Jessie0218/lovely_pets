import time
import datetime

from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login_manger


def get_timestamp():
    return int(time.time())


class BaseModel(db.Model):
    """
    基类Model，一些共有的方法
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(
        db.Integer, nullable=False, server_default=text("'0'"),
        default=get_timestamp)
    update_at = db.Column(
        db.Integer, nullable=False, server_default=text("'0'"),
        default=get_timestamp())
    deleted_at = db.Column(
        db.Integer, nullable=False, server_default=text("'0'"), default=0)

    @property
    def created_datetime(self):
        return datetime.datetime.fromtimestamp(self.created_at)

    @property
    def updated_datetime(self):
        return datetime.datetime.fromtimestamp(self.updated_at)

    @property
    def deleted_datetime(self):
        return datetime.datetime.fromtimestamp(self.deleted_at)


class Adopter(BaseModel, UserMixin):

    __tablename__ = 'adopters'

    name = db.Column(db.String(32))
    age = db.Column(db.String(32))
    mobile = db.Column(db.String(32),
                       nullable=False, default='',
                       server_default=text("'0'"))
    password =db.Column(db.String(100), nullable=False)

    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')

    @pwd.setter
    def pwd(self, password):
        self.password = generate_password_hash(password)

    def verify_pwd(self, password):
        return check_password_hash(self.password, password)


@login_manger.user_loader
def load_user(user_id):
    return Adopter.query.get(int(user_id))


class Pet(BaseModel):

    __tablename__ = 'pets'

    name = db.Column(db.String(32))
    age = db.Column(db.String(32))
    type = db.Column(db.String(32))

    adopters = db.relationship(
        'Adopter',
        primaryjoin='foreign(Pet.id)==remote(Adopter.id)',
        backref=db.backref('pets', lazy='dynamic')
    )
