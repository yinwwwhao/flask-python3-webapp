from app.views import views_blueprint as app
from flask import render_template, redirect, make_response
from func import COOKIE_NAME
from log import logging

logging.info('view/signin.py started.')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signout')
def signout():
    r = make_response(redirect('/'))
    r.delete_cookie(COOKIE_NAME)
    return r

@app.route('/register')
def register():
    return render_template('register.html')
