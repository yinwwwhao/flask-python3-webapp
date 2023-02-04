from app.manage import manage_blueprint as app
from func import check_admin, get_user
from flask import request, render_template
from log import logging

logging.info('manager/comment.py started.')

@app.route('/manage/comments')
def manage_comment():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    return render_template('manage/manage_comments.html',
                           page=page,
                           user=get_user())