# -*- coding=utf-8 -*-
from flask import Blueprint

notebook = Blueprint('notebook', __name__)

from app.notebook import routes
