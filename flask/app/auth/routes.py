from flask import request, url_for, redirect
from flask import session, render_template, jsonify
from flask_restful import Api, fields, Resource
from flask_restful import marshal_with, reqparse
from flask_login import current_user, login_user
from flask import current_app as app
from app.models import *

from app.auth import auth
from app.auth.SMSService import sendSMS
from app.auth.error import *
from app import db
import random


def login_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorator


api = Api(auth)


class LocalAuth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        auth = Auth.query.filter_by(name=args['username']).first()
        if not auth or not auth.check_password(args['password']):
            abort_wrong_login()

        user = auth.user
        login_user(user)
        return "login successfully", 200


class LocalRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('phone', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('verifycode', required=True)
        args = parser.parse_args()
        if len(args['username']) == 0 or len(args['username']) > 32:
            abort_unacceptable_length("username")
        if len(args['phone']) != 11:
            abort_unacceptable_length("phone")
        if len(args['password']) == 0:
            abort_unacceptable_length("password")
        auth = Auth.query.filter_by(name=args['username']).first()
        # if auth.verifycode != args['verifycode']:
        #     abort_wrong_verifycode()
        user = User()
        db.session.add(user)
        db.session.commit()
        auth.user = user
        auth.password_hash = Auth.get_password_hash(args['password'])
        print(args['password'],auth.password_hash)
        try:
            db.session.add(auth)
            db.session.commit()
            return 'username %s'%auth.name, 201
        except:
            db.session.rollback()

class SMSService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('phone', required=True)
        args = parser.parse_args()
        if len(args['username']) == 0 or len(args['username']) > 32:
            abort_unacceptable_length("username")
        if len(args['phone']) != 11:
            abort_unacceptable_length("phone")
        if Auth.query.filter_by(name=args['username']).first():
            abort_username_existed(args['username'])
        if Auth.query.filter_by(phone=args['phone']).first():
            abort_username_existed(args['phone'])
        try:
            code = random.randint(100000, 999999)
            auth = Auth(name=args['username'],
                        phone=args['phone'],
                        verifycode=code)
            print(auth.phone,auth.verifycode)
            ret = sendSMS(auth.phone, auth.verifycode)
            if ret['Code'] != 'OK':
                abort_send_sms_fail()
            db.session.add(auth)
            db.session.commit()
            return 'send SMS successful', 200
        except:
            db.session.rollback()
            abort_send_sms_fail()


api.add_resource(LocalRegister, '/register')
api.add_resource(LocalAuth, '/login')
api.add_resource(SMSService, '/sendSMS')
