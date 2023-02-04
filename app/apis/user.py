from app.apis import apis_blueprint as app
from app.apis._message import APIValueError, APIError
from func import datetime_filter, COOKIE_NAME, user2cookie
from flask import request, make_response, session, redirect
from app.models import User, db, next_id
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
            return APIValueError('name')
        if not email or not _RE_EMAIL.match(email):
            return APIValueError('email')
        if not passwd or not _RE_SHA1.match(passwd):
            return APIValueError('passwd')
        users = User.query.filter(User.email == email).all()
        if len(users) > 0:
            return APIError(
                'register:failed',
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
        r = redirect('/')
        r.set_cookie(COOKIE_NAME, user2cookie(
            new_user), httponly=True)
        return r
    else:
        page = int(request.args.get('page', '1'))
        p = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
        users = p.items
        for u, i in zip(users, range(len(users))):
            users[i] = u.to_dict()
            u.passwd = '******'
            users[i]['created_at'] = [
                users[i]['created_at'], datetime_filter(
                    users[i]['created_at'])]
        return dict(page={'page': p.page,
            'per_page':p.per_page,
            'total': p.total,
            'pages':p.pages,
            'first':p.first,
            'last':p.last,
            'has_prev':p.has_prev,
            'prev_num':p.prev_num,
            'has_next':p.has_next,
            'next_num':p.next_num},users=users)


@app.route('/api/authenticate', methods=['post'])
def authenticate():
    email = request.form['email']
    passwd = request.form['passwd']
    if not email:
        return APIValueError('Invalid email.')
    if not passwd:
        return APIValueError('Invalid password.')

    users = User.query.filter(User.email == email).all()
    if len(users) == 0:
        return APIValueError('Email not exist.')
    user = users[0]

    sha1 = hashlib.sha1(
        user.email.encode('utf-8') +
        b':' +
        passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        return APIValueError('Invalid password.')

    # authenticate ok, set cookie:
    r = make_response()
    r.set_cookie(
        COOKIE_NAME,
        user2cookie(user),
        httponly=True)

    return r