from app import app
from func import check_admin, get_page_index, get_user
from flask import request, render_template
from models import db, User
from apis import Page
from sqlalchemy.sql import func as sqlfunc
from log import logging

logging.info('manager/user.py started.')

@app.route('/manage/users')
def manage_user():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(sqlfunc.count(User.id)).scalar()
    p = Page(num, page_size=8)
    return render_template('manage_users.html',
                           page_index=get_page_index(page),
                           page=p,
                           user=get_user())
