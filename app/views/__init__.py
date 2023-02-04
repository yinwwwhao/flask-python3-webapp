from flask import Blueprint

views_blueprint = Blueprint('views', __name__)

from app.views import index, about, atlas, blog, signin, user