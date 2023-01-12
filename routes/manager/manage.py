from app import app
from flask import redirect
from log import logging

logging.info('manager/manage.py started.')

@app.route('/manage/')
def manage():
    return redirect('/manage/comments')