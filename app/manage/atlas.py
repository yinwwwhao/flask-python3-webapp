from app.manage import manage_blueprint as app
from func import check_admin, get_user
from app.models import Atlas
from flask import request, render_template
from log import logging

logging.info('manager/atlas.py started.')

@app.route('/manage/atlas')
def manage_atlas():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    return render_template('manage/manage_atlas.html', 
                page=page, 
                user=get_user())

