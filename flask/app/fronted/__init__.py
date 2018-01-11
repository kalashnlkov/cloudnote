# -*- coding=utf-8 -*-
from flask import Blueprint

fronted = Blueprint('fronted', __name__,
                    template_folder='templates',
                    static_folder='../static',
                    static_url_path='/f')

from app.fronted import routes