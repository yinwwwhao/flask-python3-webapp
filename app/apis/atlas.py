from app.apis import apis_blueprint as app
from app.apis._message import APIValueError, Message
from func import check_admin, datetime_filter
import os
from flask import request
from app.models import Atlas, db
from log import logging
import base64
import time

logging.info('api/atlas.py started.')
filepath = os.path.join(*'static/images/atlas/a'.split('/'))[:-1]

@app.route('/api/atlas/delete', methods=['POST'])
def api_delete_atlas():
    if check_admin():
        return check_admin()
    url = request.form.get('url')
    if not url or not url.strip():
        return APIValueError('url')
    Atlas.query.filter(Atlas.url == url).delete()
    db.session.commit()
    os.remove(os.path.join(*url[1:].split('/')))
    return Message('delete ok')


@app.route('/api/atlas/create', methods=['POST'])
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
        return APIValueError('data')
    if not name or not name.strip():
        return APIValueError('name')
    if not filetype or not filetype.strip():
        return APIValueError('filetype')

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
    return Message('create or update atlas ok')


@app.route('/api/atlas')
def api_get_atlas():
    page = int(request.args.get('page', 1))
    p = Atlas.query.order_by(
    Atlas.created_at.desc()).paginate(page=page, per_page=10)
    atlas = p.items
    for a in range(len(atlas)):
        atlas[a] = atlas[a].to_dict()
        atlas[a]['created_at'] = [
            atlas[a]['created_at'], datetime_filter(
                atlas[a]['created_at'])]
    return dict(page={
            'page': p.page,
            'per_page':p.per_page,
            'total': p.total,
            'pages':p.pages,
            'first':p.first,
            'last':p.last,
            'has_prev':p.has_prev,
            'prev_num':p.prev_num,
            'has_next':p.has_next,
            'next_num':p.next_num
        }, atlas=atlas)

@app.route('/api/atlas/rename', methods=['POST'])
def rename_atlas():
    name = request.form.get('name')
    newname = request.form.get('newname')
    if not name or not newname:
        return APIValueError('name')
    
    t = '.jpg'
    for imgname in os.listdir('static/images/atlas'):
        if '.'.join(imgname.split('.')[:-1]) == name:
            t = imgname.split('.')[-1]
            logging.info(filepath+name+'.'+t, filepath+newname + '.' + t)
            os.rename(filepath+name+'.'+t, filepath+newname + '.' + t)
    Atlas.query.filter(Atlas.name == name).update({
        'name': newname,
        'created_at': time.time(),
        'url': f'/static/images/atlas/{newname}.{t}'
    })
    db.session.commit()
    return Message('rename ok')



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
    return Message('update ok')


