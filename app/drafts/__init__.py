from flask import Blueprint

drafts = Blueprint('drafts', __name__)

from . import routes