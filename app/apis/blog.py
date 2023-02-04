from app.apis import apis_blueprint as app
from app.apis._message import APIValueError, Message
from func import check_admin, datetime_filter, get_user
from flask import request, abort
from app.models import Blog, db, Comment
from log import logging
import time

logging.info('api/blog.py started.')

@app.route('/api/blogs/<id>/delete', methods=['POST'])
def delete_blog(id):
    if check_admin():
        return check_admin()
    Blog.query.filter(Blog.id == id).delete()
    Comment.query.filter(Comment.blog_id == id).delete()
    db.session.commit()
    return Message('delete ok')

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
            return APIValueError('name cannot be empty.')
        if not request.form['summary'] or not request.form['summary'].strip():
            return APIValueError('summary cannot be empty.')
        if not request.form['content'] or not request.form['content'].strip():
            return APIValueError('content cannot be empty.')
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
        page = int(request.args.get('page', 1))
        p = Blog.query.order_by(
            Blog.created_at.desc()).paginate(page=page, per_page=5)
        blogs = p.items
        for b in range(len(blogs)):
            blogs[b] = blogs[b].to_dict()
            blogs[b]['created_at'] = [
                blogs[b]['created_at'], datetime_filter(
                    blogs[b]['created_at'])]
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
        }, blogs=blogs)
