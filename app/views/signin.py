from app.views import views_blueprint as app
from flask import session, request, render_template, make_response
from func import COOKIE_NAME, send_email
import random
from log import logging

logging.info('view/signin.py started.')

@app.route('/get_verification', methods=['post'])
def get_verification():
    return str(session.get(request.form.get('email')))


@app.route('/send_verification', methods=['post'])
def send_verification():
    verification = random.randint(0, 999999)
    session[request.form.get('email')] = verification
    send_email(verification, request.form.get('email'))
    return 'send ok'


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signout')
def signout():
    r = make_response("<script>location.assign('/');</script>")
    r.delete_cookie(COOKIE_NAME)
    return r

@app.route('/register')
def register():
    return render_template('register.html')
