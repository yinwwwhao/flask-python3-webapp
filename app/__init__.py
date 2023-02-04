from flask import Flask
from app.extensions import db
import configs
from log import logging
from app.apis import apis_blueprint
from app.views import views_blueprint
from app.manage import manage_blueprint
from func import datetime_filter
def create_app():
    logging.info('start app.')
    app = Flask(__name__)

    app.config.from_object(configs)
    db.init_app(app)

    app.register_blueprint(apis_blueprint)
    app.register_blueprint(views_blueprint)
    app.register_blueprint(manage_blueprint)
    app.add_template_filter(datetime_filter, 'datetime')
    logging.info('app is running...')
    return app
