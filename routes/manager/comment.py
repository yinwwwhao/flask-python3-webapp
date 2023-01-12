from app import app
from func import check_admin, get_page_index, get_user
from flask import request, render_template
from sqlalchemy.sql import func as sqlfunc
from models import Comment, db
from apis import Page
from log import logging

logging.info('manager/comment.py started.')

@app.route('/manage/comments')
def manage_comment():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(sqlfunc.count(Comment.id)).scalar()
    p = Page(num, page_size=10)

    return render_template('manage_comments.html',
                           page_index=get_page_index(page),
                           page=p,
                           user=get_user())