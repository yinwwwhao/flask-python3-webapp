from app import app
from flask import request, render_template, redirect, abort
from sqlalchemy.sql import func as sqlfunc
from func import get_user
from models import db, Atlas
from apis import Page
from log import logging

logging.info('view/atlas started.')

@app.route('/atlas/public')
def atlas():
    page = int(request.args.get('page', 1))
    user = get_user()
    num = db.session.query(sqlfunc.count(Atlas.name)).filter(
        False == Atlas.private).scalar()
    p = Page(num, page_size=20, page_index=page)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self().order_by(Atlas.created_at.desc()).filter(Atlas.private == False).all()
    return render_template('atlas.html', user=user, image=image, page=p)


@app.route('/atlas')
def atlas_redirect():
    return redirect('/atlas/public')


@app.route('/atlas/private')
def atlas_private():
    user = get_user()
    if not user:
        pass
    elif user.admin != True:
        return abort(403)
    else:
        pass
    page = int(request.args.get('page', 1))
    user = get_user()
    num = db.session.query(sqlfunc.count(Atlas.name)).filter(
        True == Atlas.private).scalar()
    p = Page(num, page_size=20, page_index=page)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self().order_by(Atlas.created_at.desc()).filter(Atlas.private == True).all()
    return render_template('atlas_private.html', user=user, image=image, page=p)
