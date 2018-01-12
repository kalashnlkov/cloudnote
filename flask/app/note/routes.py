# -*- coding=utf-8 -*-
from flask_restful import Api, fields, Resource
from flask_restful import marshal_with, reqparse
from flask_login import current_user

from app.note import note
from app.note.error import *
from app.models import Note, Notebook
from app import db


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
    "title": fields.String,
    "content": fields.String,
    "like": fields.Integer,
    "view": fields.Integer
}

# class NoteList(Resource):
#     """
#     do (get,insert)
#     """
#     def get(self,):
#         notelist =


class NoteList(Resource):
    """do get note list or insert new note
    """
    @marshal_with(note_fields, envelope='note')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('notebookid')
        args = parser.parse_args()
        print(args['notebookid'])
        if not args['notebookid'].isdigit():
            abort_datatype_error('notebookid')
        note = Note.query.filter_by(
            notebook_id=args['notebookid']).all()
        if len(note) > 0:
            return note
        abort_id_cannot_found("notebookid")



    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')
        parser.add_argument('notebookid')
        args = parser.parse_args()
        print(current_user, args['title'])
        if not args['notebookid'].isdigit():
                abort_datatype_error('notebookid')
        notebook= Notebook.query.filter_by(user=current_user,
                                    id=args['notebookid']).first()
        if not notebook:
            abort_id_cannot_found('notebookid ' + args['notebookid'])
        if len(args['title']) == 0 or len(args['title']) > 32:
            abort_unacceptable_length('title')
        if len(args['content']) > 512:
            abort_unacceptable_length('content')
        new_note = Note(title=args['title'],
                        content=args['content'],
                        notebook=notebook)
        db.session.add(new_note)
        db.session.commit()
        return "new note(%s) success" % args['title'], 201


class NoteDetail(Resource):
    """
    do (search,update,delete)
    """
    # TODO
    # method_decorators = [login_required]
    def get_object(self, id):
        """check creater before return object"""
        print(current_user)
        notebook = Notebook.query.filter_by(
            user=current_user
        ).all()
        note = Note.query.filter(
            Note.notebook_id.in_(
                [nb.id for nb in notebook]),
            Note.id == id
        ).first()
        if not note:
            abort_id_cannot_found('')
        return note
    @marshal_with(note_fields)
    def get(self, id):
        note = self.get_object(id)
        return note

    def delete(self, id):
        note = self.get_object(id)
        db.session.delete(note)
        db.session.commit()
        return 'delete note ' + id, 204
    @marshal_with(note_fields)
    def put(self, id):
        note = self.get_object(id)

        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()

        if args['content'] is not None:
            if len(args['content']) > 512:
                abort_unacceptable_length('content')
        if args['title'] is not None:
            if len(args['title']) > 32:
                abort_unacceptable_length('title')
        if args['content']:
            note.content = args['content']
        if args['title']:
            note.title = args['title']
        db.session.commit()
        return note, 201


api.add_resource(NoteList, '')
api.add_resource(NoteDetail, '/<id>')
