from flask import Blueprint

manage_blueprint = Blueprint('manage', __name__)

from app.manage import atlas, blog, comment, manage, user