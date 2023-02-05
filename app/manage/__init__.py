from flask import Blueprint
from flask import redirect

manage_blueprint = Blueprint('manage', __name__)

@manage_blueprint.route('/manage/')
def manage():
    return redirect('/manage/comments')

from app.manage import atlas, blog, comment, manage, user