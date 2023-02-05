from app.manage import manage_blueprint as app
from func import check_admin, get_user
from flask import render_template
from log import logging

logging.info('manager/user.py started.')

@app.route('/manage/users')
def manage_user():
    admin = check_admin()
    if admin:
        return admin
    return render_template('manage/manage_users.html',
                           user=get_user())
