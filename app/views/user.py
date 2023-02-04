from app.views import views_blueprint as app
from app.models import User
from log import logging

logging.info('view/user.py started.')

@app.route('/users/<id>')
def user_index(id):
    user = User.query.filter(User.id == id).one()
    return f'<h2>暂未开放，{user.name}！<br />如有需求请联系尹伟豪在数据库中操作。<a href="/"><br />回到主页</a></h2>'
