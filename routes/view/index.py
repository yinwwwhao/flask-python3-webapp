from app import app
from flask import request, render_template
from models import db, Blog
from func import get_user, get_tag
from apis import Page
from sqlalchemy.sql import func as sqlfunc

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    if request.args.get('tag', None):
        num = db.session.query(sqlfunc.count(Blog.id)).scalar()
        p = Page(num, page_size=5, page_index=page)
        blogs = Blog.query.offset(
            p.offset).limit(
            p.limit).from_self(
        ).filter(
            Blog.tag == request.args.get('tag', None)
        ).order_by(
            Blog.created_at.desc()).all()
        user = get_user()
        return render_template('index.html', blogs=blogs, user=user, title=request.args.get('tag', None), tags=get_tag(), page=p, tag=request.args.get('tag', None))
    else:
        num = db.session.query(sqlfunc.count(Blog.id)).scalar()
        p = Page(num, page_size=8, page_index=page)
        user = get_user()
        blogs = Blog.query.offset(
            p.offset).limit(
            p.limit).from_self().order_by(
            Blog.created_at.desc()).all()
        return render_template('index.html',
                               user=user,
                               blogs=blogs,
                               title='首页',
                               tags=get_tag(),
                               page=p)