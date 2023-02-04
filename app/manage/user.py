from app.manage import manage_blueprint as app
from func import check_admin, get_user
from flask import request, render_template
from log import logging

logging.info('manager/user.py started.')

@app.route('/manage/users')
def manage_user():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    return render_template('manage/manage_users.html',
                           page=page,
                           user=get_user())
