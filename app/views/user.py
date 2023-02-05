from app.views import views_blueprint as app
from app.models import User
from log import logging
from flask import render_template, redirect
from func import get_user

logging.info('view/user.py started.')

@app.route('/users/<id>')
def user_index(id):
    user = User.query.filter(User.id == id).one()
    return render_template('user.html',user=get_user(), userobj=user)

@app.route('/me')
def me():
    user = get_user()
    return render_template('me.html', user=user)