from waitress import serve
from app import app
from routes.view import about, atlas, blog, signin, user, index
from routes.manager import atlas, blog, comment, manage, user
from routes.apis import atlas, blog, comment, user
from configs import mode

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        serve(app, host='localhost', port=8000)