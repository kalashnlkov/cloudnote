# -*- coding=utf-8 -*-
from app import db
import datetime
from werkzeug.security import generate_password_hash as GPH
from werkzeug.security import check_password_hash as CPH

class Base():
    """Base class provide get_id"""
    def get_id(self):
        """return self.id"""
        return self.id

class User(Base, db.Model):
    """Table User"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(93))
    gender = db.Column(db.Boolean())
    city = db.Column(db.String(128))
    birthday = db.Column(db.DateTime())
    email = db.Column(db.String(128))
    phone = db.Column(db.String(11))
    is_registed = db.Column(db.Boolean(),default=False)
    notebooks = db.relationship("Notebook",
                                backref="user",
                                lazy="dynamic")
    auths = db.relationship("Auth",
                            backref="user",
                            lazy="dynamic")
    def __init__(self, name, password_hash, phone, gender=None,
                 city=None, birthday=None, email=None,is_registed=False):
        self.name = name
        self.set_password(password_hash)
        self.gender = gender
        self.city = city
        self.birthday = birthday
        self.email = email
        self.phone = phone
        self.is_registed = is_registed
    def set_password(self,password):
        self.password_hash = GPH(password)
        print('sethash',self.password_hash)
    def check_password(self, password):
        return CPH(self.password_hash, password)
    def regist(self):
        self.is_registed = True

class Auth(db.Model):
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"),
                        primary_key=True)
    verifycode = db.Column(db.String(6))

class Notebook(Base, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(32), unique=True)
    content = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))
    notes = db.relationship("Note",
                           backref="notebook",
                           lazy="dynamic")
    def __init__(self,title):
        self.title = title

class Note(Base, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(32), unique=True)
    content = db.Column(db.String(512), nullable=True)
    like = db.Column(db.Integer(), default=0)
    view = db.Column(db.Integer(), default=0)
    notebook_id = db.Column(db.Integer(),
                            db.ForeignKey("notebook.id"))
    def __init__(self,title):
        self.title = title
