from app.apis import apis_blueprint as app
from app.apis._message import APIValueError, Message, APIPermissionError
from func import check_admin, datetime_filter
import os
from flask import request
from app.models import Atlas, db, next_id
from log import logging
import base64

logging.info('api/atlas.py started.')
filepath = 'app/static/images/atlas/'

@app.route('/api/atlas/delete', methods=['POST'])
def api_delete_atlas():
    admin = check_admin()
    if admin:
        return APIPermissionError('permission error')
    id = request.form.get('id')
    if not id or not id.strip():
        return APIValueError('id')
    atlas = Atlas.query.filter(Atlas.id == id)
    os.remove(filepath+id+'.'+atlas.one().image_type)
    atlas.delete()
    db.session.commit()
    return Message('delete ok')


@app.route('/api/atlas/create', methods=['POST'])
def api_create_atlas():
    admin = check_admin()
    if admin:
        return APIPermissionError('permission error')
    id = next_id()
    data = request.form.get('data')
    private = request.form.get('private') == 'true'
    filetype = request.form.get('filetype')
    
    if not data or not data.strip():
        return APIValueError('data')
    if not filetype or not filetype.strip():
        return APIValueError('filetype')


    data = base64.b64decode(data)
    with open(filepath+'{0}.{1}'.format(id, filetype), 'wb') as f:
        f.write(data)

    new_atlas = Atlas(
        url='/static/images/atlas/{0}.{1}'.format(id, filetype),
        id=id,
        image_type=filetype,
        private=private,
    )
    db.session.add(new_atlas)
    db.session.commit()
    return Message('create atlas ok')


@app.route('/api/atlas')
def api_get_atlas():
    page = int(request.args.get('page', 1))
    p = Atlas.query.order_by(
    Atlas.created_at.desc()).paginate(page=page, per_page=12)
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



@app.route('/api/atlas/private', methods=['POST'])
def private_atlas():
    private = request.form.get('private')
    id = request.form.get('id')
    if private == 'false':
        private = False
    else:
        private = True
    Atlas.query.filter(Atlas.id == id).update({
        'private': private
    })
    db.session.commit()
    return Message('update ok')


