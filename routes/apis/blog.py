from app import app
from apis import APIValueError, Page
from func import check_admin, datetime_filter, get_page_index, get_user
from flask import request, abort
from models import Blog, db, Comment
from log import logging
from sqlalchemy.sql import func as sqlfunc
import time

logging.info('api/blog.py started.')

@app.route('/api/blogs/<id>/delete', methods=['POST'])
def delete_blog(id):
    if check_admin():
        return check_admin()
    Blog.query.filter(Blog.id == id).delete()
    Comment.query.filter(Comment.blog_id == id).delete()
    db.session.commit()
    return 'delete ok'

@app.route('/api/blogs/<id>')
def api_get_blog(id):
    blog = Blog.query.filter(Blog.id == id).one().to_dict()
    return blog

@app.route('/api/blogs', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        if check_admin():
            return check_admin()
        user = get_user()
        if not user:
            return abort(403)
        if not request.form['name'] or not request.form['name'].strip():
            raise APIValueError('name', 'name cannot be empty.')
        if not request.form['summary'] or not request.form['summary'].strip():
            raise APIValueError('summary', 'summary cannot be empty.')
        if not request.form['content'] or not request.form['content'].strip():
            raise APIValueError('content', 'content cannot be empty.')
        if request.form.get('id'):
            Blog.query.filter(Blog.id == request.form.get('id')).update({
                'name': request.form['name'].strip(),
                'summary': request.form['summary'].strip(),
                'content': request.form['content'].strip(),
                'created_at': time.time(),
                'tag': request.form['tag'].strip()
            })
            db.session.commit()
            blog = Blog.query.filter(
                Blog.id == request.form['id']).one()
            return blog.to_dict()
        else:
            new_blog = Blog(
                user_id=user.id,
                user_name=user.name,
                user_image=user.image,
                name=request.form['name'].strip(),
                summary=request.form['summary'].strip(),
                content=request.form['content'].strip(),
                tag=request.form['tag'].strip()
            )
            db.session.add(new_blog)
            db.session.commit()
        return new_blog.to_dict()
    else:
        page = request.args.get('page', 1)
        page_index = get_page_index(page)
        num = db.session.query(sqlfunc.count(Blog.id)).scalar()
        p = Page(num, page_index)
        if num == 0:
            return dict(page=p.__dict__, blogs=())
        blogs = Blog.query.offset(
            p.offset).limit(
            p.limit).from_self().order_by(
            Blog.created_at.desc()).all()
        for b in range(len(blogs)):
            blogs[b] = blogs[b].to_dict()
            blogs[b]['created_at'] = [
                blogs[b]['created_at'], datetime_filter(
                    blogs[b]['created_at'])]
        return dict(page=p.__dict__, blogs=blogs)
