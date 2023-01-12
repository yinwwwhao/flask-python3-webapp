from app import app
from func import get_user
from flask import render_template
from log import logging

logging.info('view/about.py started.')

@app.route('/about')
def about():
    return render_template('about.html', user=get_user())
