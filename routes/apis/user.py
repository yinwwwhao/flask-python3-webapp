from app import app
from apis import APIValueError, APIError
from func import datetime_filter, COOKIE_NAME, user2cookie
from flask import request, make_response, session
from models import User, db, next_id
from log import logging
import hashlib
import re


logging.info('api/user.py started.')


_RE_EMAIL = re.compile(
    r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@app.route('/api/users', methods=['get', 'post'])
def user():
    if request.method == 'POST':

        email = request.form['email']
        name = request.form['name']
        passwd = request.form['passwd']

        if not name or not name.strip():
            raise APIValueError('name')
        if not email or not _RE_EMAIL.match(email):
            raise APIValueError('email')
        if not passwd or not _RE_SHA1.match(passwd):
            raise APIValueError('passwd')
        users = User.query.filter(User.email == email).all()
        if len(users) > 0:
            raise APIError(
                'register:failed',
                'email',
                'Email is already in use.')
        uid = next_id()
        new_user = User(id=uid, name=name.strip(), email=email,
                        passwd=passwd,
                        image='/static/images/user.svg',
                        admin=True)
        db.session.add(new_user)
        db.session.commit()

        del session[request.form.get('email')]
        # make session cookie:
        r = make_response("<script>location.assign('/');</script>")
        r.set_cookie(COOKIE_NAME, user2cookie(
            new_user), httponly=True)
        return r
    else:
        users = User.query.order_by(User.created_at.desc()).all()
        for u, i in zip(users, range(len(users))):

            users[i] = u.to_dict()
            u.passwd = '******'
            users[i]['created_at'] = [
                users[i]['created_at'], datetime_filter(
                    users[i]['created_at'])]
        return dict(users=users)


@app.route('/api/authenticate', methods=['post'])
def authenticate():
    email = request.form['email']
    passwd = request.form['passwd']
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')

    users = User.query.filter(User.email == email).all()
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]

    sha1 = hashlib.sha1(
        user.email.encode('utf-8') +
        b':' +
        passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')

    # authenticate ok, set cookie:
    r = make_response()
    r.set_cookie(
        COOKIE_NAME,
        user2cookie(user),
        httponly=True)

    return r