from flask_restful import Api, fields, Resource
from flask_restful import marshal_with, reqparse
from flask_login import current_user

from app.note import note
from app.models import Note, Notebook
from app import db


# login 验证
def login_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorator
api = Api(note)

note_fields = {
    "id": fields.Integer,
    "title":fields.String,
    "content": fields.String,
    "like": fields.Integer,
    "view": fields.Integer
}

class Notebook(Resource):
    """
    get list of note, or new a note
    """
    method_decorators = [login_required]
    @marshal_with(note_fields, envelope='note')
    def get(self):
        notes = Note
class Note(Resource):
    """
    do (search,update,delete)
    """
    method_decorators = [login_required]
    @marshal_with(note_fields, envelope='note')
    def get(self):