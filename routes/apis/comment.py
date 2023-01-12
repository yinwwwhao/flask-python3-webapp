from app import app
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, Page
from func import check_admin, datetime_filter, get_page_index, get_user
from flask import request
from models import Comment, db, Blog
from log import logging
from sqlalchemy.sql import func as sqlfunc

logging.info('api/comment.py started.')

@app.route('/api/comments/<id>/delete', methods=['POST'])
def delete_comment(id):
    if check_admin():
        return check_admin()
    Comment.query.filter(Comment.id == id).delete()
    db.session.commit()
    return 'delete ok'

@app.route('/api/comments')
def api_comments():
    page = request.form.get('page', 1)
    page_index = get_page_index(page)
    num = db.session.query(sqlfunc.count(Blog.id)).scalar()
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p.__dict__, comments=())
    comments = Comment.query.offset(
        p.offset).limit(
        p.limit).from_self().order_by(
        Comment.created_at.desc()).all()
    for b in range(len(comments)):
        comments[b] = comments[b].to_dict()
        comments[b]['created_at'] = [
            comments[b]['created_at'], datetime_filter(
                comments[b]['created_at'])]
    return dict(page=p.__dict__, comments=comments)

@app.route('/api/blogs/<id>/comments', methods=['POST'])
def api_create_comment(id):
    user = get_user()
    content = request.form.get('content', None)
    if user is None:
        raise APIPermissionError('Please sign in first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = Blog.query.filter(Blog.id == id).one()
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, 
    user_name=user.name, user_image=user.image,
                      content=content.strip())
    db.session.add(comment)
    db.session.commit()
    return comment.to_dict()
