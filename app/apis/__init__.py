from flask import Blueprint

apis_blueprint = Blueprint('apis', __name__)

from app.apis import atlas, blog, comment, user