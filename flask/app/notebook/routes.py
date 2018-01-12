from flask_restful import Api, fields, Resource
from flask_restful import marshal_with, reqparse
from flask_login import current_user

from app.notebook import notebook
from app.notebook.error import *
from app.models import Notebook
from app import db



def login_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorator
api = Api(notebook)

notebook_fields = {
    "id": fields.Integer,
    "title":fields.String,
    "content": fields.String,
    "user_id": fields.Integer
}

class NoteBookList(Resource):
    """
        do get notebooklist or insert 
    """
    method_decorators = [login_required]
    @marshal_with(notebook_fields, envelope='notebook')
    def get(self):
        notebook = Notebook.query.filter_by(user=current_user).all()
        return notebook
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        print(current_user,args['title'])
        if Notebook.query.filter_by(user=current_user,
                            title=args['title']).first():
            abort_item_exsist('Notebook '+args['title'])
        if len(args['title']) ==0 or len(args['title']) > 32:
            abort_unacceptable_length('title')
        if len(args['content']) ==0 or len(args['content']) > 64:
            abort_unacceptable_length('content')
        new_notebook = Notebook(title=args['title'],
                                content=args['content'],
                                user=current_user)
        db.session.add(new_notebook)
        db.session.commit()
        return "new notebook(%s) success"%args['title'],201
class NoteBookDetail(Resource):
    """
    do (search,update,delete)
    """
    method_decorators = [login_required]
    def get_object(self, id):
        notebook = Notebook.query.filter_by(
            id=id,
            user=current_user
        ).first()
        if not notebook:
            abort_id_cannot_found()
        return notebook

    @marshal_with(notebook_fields)
    def get(self, id):
        notebook = self.get_object(id)
        return notebook

    def delete(self,id):
        notebook = self.get_object(id)
        db.session.delete(notebook)
        db.session.commit()
        return 'delete notebook ' + id, 204

    def put(self, id):
        notebook = self.get_object(id)

        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('content')
        args = parser.parse_args()
        if args['content'] is not None:
            if len(args['content']) > 64:
                abort_unacceptable_length('content')
        if args['title'] is not None:
            if len(args['title']) > 32:
                abort_unacceptable_length('title')
        if args['content']:
            notebook.content = args['content']
        if args['title']:
            notebook.title = args['title']
        db.session.commit()
        return notebook, 201

api.add_resource(NoteBookList, '')
api.add_resource(NoteBookDetail, '/<id>')