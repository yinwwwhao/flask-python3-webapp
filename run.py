from waitress import serve
from app import app
from routes.view import about, atlas, blog, signin, user, index
from routes.manager import atlas, blog, comment, manage, user
from routes.apis import atlas, blog, comment, user
from configs import mode as m
from sys import argv

def parse_args():
    args = {}
    for i in range(len(argv)):
        if argv[i] == '-h' and len(argv) != i+1:
            args['host'] = argv[i+1]
        if argv[i] == '-p' and len(argv) != i+1:
            args['port'] = int(argv[i+1])
        if argv[i] == '-m' and len(argv) != i+1:
            args['mode'] = argv[i+1]
    return args




if __name__ == '__main__':
    args = parse_args()
    host = args.get('host', 'localhost')
    port = args.get('port', 8000)
    mode = args.get('mode', m)
    if mode == 'dev':
        app.run(host=host, port=port, debug=True)
    else:
        serve(app, host=host, port=port)
