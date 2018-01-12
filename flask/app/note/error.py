from flask_restful import abort


def abort_unacceptable_length(attr_name):
    abort(400, message="%s is unacceptable length"%(attr_name))

def abort_datatype_error(item):
    abort(400, message="%s type error" % item)
def abort_id_cannot_found(item):
    abort(404, message="%s can't found" % item)

def abort_role_limitation(role_name, limitation):
    abort(400, message="%s only can have %i to do task"%(role_name,limitation))
