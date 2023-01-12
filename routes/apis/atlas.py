from app import app
from apis import APIValueError
from func import check_admin
import os
from flask import request
from models import Atlas, db
from log import logging
import base64
import time

logging.info('api/atlas.py started.')

@app.route('/api/atlas/delete', methods=['POST'])
def api_delete_atlas():
    if check_admin():
        return check_admin()
    url = request.form.get('url')
    if not url or not url.strip():
        raise APIValueError('url')
    Atlas.query.filter(Atlas.url == url).delete()
    db.session.commit()
    os.remove(os.path.join(*url[1:].split('/')))
    return 'delete ok'


@app.route('/api/atlas', methods=['POST'])
def api_create_atlas():
    if check_admin():
        return check_admin()

    data = request.form.get('data')
    name = request.form.get('name')
    private = request.form.get('private')
    if private == 'false':
        private = False
    else:
        private = True
    filetype = request.form.get('filetype')
    if not data or not data.strip():
        raise APIValueError('data')
    if not name or not name.strip():
        raise APIValueError('name')
    if not filetype or not filetype.strip():
        raise APIValueError('filetype')

    for x in os.listdir('static/images/atlas/'):
        if os.path.isfile(x):
            if x.split('.')[-1] != filetype:
                os.rename(f'static/images/atlas/{x}', 'static/images/atlas/{}'.format(
                '.'.join(x.split('.')[:-1])+'.'+filetype))
    data = base64.b64decode(data)
    with open('static/images/atlas/{0}.{1}'.format(name, filetype), 'wb') as f:
        f.write(data)

    if not Atlas.query.filter(Atlas.name == name).all():
        image = Atlas(
            name=name, url='/static/images/atlas/{0}.{1}'.format(name, filetype), private=private)
        db.session.add(image)
        db.session.commit()
    else:
        Atlas.query.filter(Atlas.name == name).update({
            'name': name,
            'url': '/static/images/atlas/{0}.{1}'.format(name, filetype),
            'private': private,
            'created_at': time.time()
        })
        db.session.commit()
    return 'create or update atlas ok'

@app.route('/api/atlas/rename', methods=['POST'])
def rename_atlas():
    name = request.form.get('name')
    newname = request.form.get('newname')
    if not name or not newname:
        raise APIValueError('name')
    
    t = 'jpg'
    for x in os.listdir('static/images/atlas'):
        print('.'.join(x.split('.')[:-1])*10000000)
        if '.'.join(x.split('.')[:-1]) == newname:
            t = x.split('.')[-1]
            os.rename(x, newname + '.' + x.split('.')[-1])
    Atlas.query.filter(Atlas.name == name).update({
        'name': newname,
        'created_at': time.time(),
        'url': f'/static/images/atlas/{newname}.{t}'
    })
    db.session.commit()
    return 'rename ok'



@app.route('/api/atlas/private', methods=['POST'])
def private_atlas():
    private = request.form.get('private')
    name = request.form.get('name')
    if private == 'false':
        private = False
    else:
        private = True
    Atlas.query.filter(Atlas.name == name).update({
        'private': private
    })
    db.session.commit()
    return 'update ok'


