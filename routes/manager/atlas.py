from app import app
from func import check_admin, get_user
from sqlalchemy.sql import func as sqlfunc
from models import Atlas, db
from flask import request, render_template
from apis import Page
from log import logging

logging.info('manager/atlas.py started.')

@app.route('/manage/atlas')
def manage_atlas():
    if check_admin():
        return check_admin()
    page = int(request.args.get('page', 1))
    num = db.session.query(sqlfunc.count(Atlas.url)).scalar()
    p = Page(num, page_index=page, page_size=8)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self(
    ).order_by(
            Atlas.created_at.desc()).all()
    return render_template('manage_atlas.html', 
                page=p, 
                image=image,
                user=get_user())

