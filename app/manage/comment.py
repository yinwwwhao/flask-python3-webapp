from app.manage import manage_blueprint as app
from func import check_admin, get_user
from flask import render_template
from log import logging

logging.info('manager/comment.py started.')

@app.route('/manage/comments')
def manage_comment():
    admin = check_admin()
    if admin:
        return admin
    return render_template('manage/manage_comments.html',
                           user=get_user())