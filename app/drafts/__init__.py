from flask import Blueprint

posts = Blueprint('drafts', __name__)

from . import routes