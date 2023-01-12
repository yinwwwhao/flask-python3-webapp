from flask import Flask
import sql_configs
from models import db
from log import logging
from func import datetime_filter

app = Flask(__name__)
app.config.from_object(sql_configs)
db.init_app(app)

app.add_template_filter(datetime_filter, 'datetime')
logging.info('Flask app created.')


