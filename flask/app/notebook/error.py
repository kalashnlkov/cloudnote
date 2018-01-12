from flask_restful import abort


def abort_unacceptable_length(attr_name):
    abort(400, message="%s is unacceptable length"%(attr_name))


def abort_id_cannot_found():
    abort(404, message="current user owns no such notebook")


def abort_role_limitation(role_name, limitation):
    abort(400, message="%s only can have %i to do task"%(role_name,limitation))

def abort_item_exsist(item):
    abort(400, message="%s already exsis"%item)