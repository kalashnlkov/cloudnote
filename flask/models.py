# -*- coding=utf-8 -*-
from app import db
import datetime

class Base():
    """Base class provide get_id"""
    def get_id(self):
        """return self.id"""
        return self.id

class User(Base, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(93))
    gender = db.Column(db.Boolean())
    city = db.Column(db.String(128))
    birthday = db.Column(db.DateTime())
    email = db.Column(db.String(128))
    notebooks = db.relationship("Notebook",
                               backref="user",
                               lazy="dynamic")

    def __init__(self, name, password_hash, gender=None,
                 city=None, birthday=None, email=None):
        self.name = name
        self.password_hash = password_hash
        self.gender = gender
        self.city = city
        self.birthday = birthday
        self.email = email

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
    notebook_id = db.Column(db.Integer(),
                            db.ForeignKey("notebook.id"))
    def __init__(self,title):
        self.title = title
