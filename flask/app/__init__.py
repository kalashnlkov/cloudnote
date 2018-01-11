# -*- coding=utf-8 -*-
from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "basic"
login_manager.login_view = "auth.index"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.fronted import fronted as fronted_blueprint
    app.register_blueprint(fronted_blueprint)
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('frontend.login'))
