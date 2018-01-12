# -*- coding=utf-8 -*-
from app import db
import datetime
from werkzeug.security import generate_password_hash as GPH
from werkzeug.security import check_password_hash as CPH
from flask_login import UserMixin


class Base():
    """Base class provide get_id"""

    def get_id(self):
        """return self.id"""
        return self.id


class User(Base, db.Model, UserMixin):
    """Table User"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)

    gender = db.Column(db.Boolean())
    city = db.Column(db.String(128))
    birthday = db.Column(db.DateTime())
    email = db.Column(db.String(128))
    phone = db.Column(db.String(11))
    is_registed = db.Column(db.Boolean(), default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.is_authenticated
    # notebooks = db.relationship("Notebook",
    #                             backref="user",
    #                             lazy="dynamic")
    # auths = db.relationship("Auth",
    #                         backref="user",
    #                         lazy="dynamic")

    def __init__(self, name=None, phone=None, gender=None,
                 city=None, birthday=None, email=None,
                 is_registed=False):
        self.name = name
        self.gender = gender
        self.city = city
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.is_registed = is_registed

    def regist(self):
        self.is_registed = True


class Auth(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))
    verifycode = db.Column(db.String(6))
    name = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(93))
    phone = db.Column(db.String(11))
    verify_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    user = db.relationship("User",
                           backref=db.backref('auth', lazy='dynamic'))

    def __init__(self, user=None, name=None, password=None,
                 verifycode=None, phone=None):
        self.user = user
        self.name = name
        self.password_hash = self.get_password_hash(password)
        self.verifycode = verifycode
        self.phone = phone

    def get_password_hash(password=None):
        if password is None:
            return None
        return GPH(password)

    def check_password(self, password):
        return CPH(self.password_hash, password)


class Notebook(Base, db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(32), unique=True)
    content = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))
    # notes = db.relationship("Note",
    #                        backref="notebook",
    #                        lazy="dynamic")
    user = db.relationship("User",
                           backref=db.backref('notebook', lazy='dynamic'))

    def __init__(self, title,content,user):
        self.title = title
        self.content = content
        self.user = user


class Note(Base, db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(32), unique=True)
    content = db.Column(db.String(512), nullable=True)
    like = db.Column(db.Integer(), default=0)
    view = db.Column(db.Integer(), default=0)
    notebook_id = db.Column(db.Integer(),
                            db.ForeignKey("notebook.id"))
    notebook = db.relationship("Notebook",
                                backref=db.backref('note', lazy='dynamic'))
    def __init__(self, title, content=None,notebook=None):
        self.title = title
        self.content = content
        self.notebook = notebook
