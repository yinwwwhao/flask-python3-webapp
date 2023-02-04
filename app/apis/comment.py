from app.apis import apis_blueprint as app
from app.apis._message import APIValueError, APIResourceNotFoundError, APIPermissionError, Message
from func import check_admin, datetime_filter, get_user
from flask import request
from app.models import Comment, db, Blog
from log import logging

logging.info('api/comment.py started.')

@app.route('/api/comments/<id>/delete', methods=['POST'])
def delete_comment(id):
    if check_admin():
        return check_admin()
    Comment.query.filter(Comment.id == id).delete()
    db.session.commit()
    return Message('delete ok')

@app.route('/api/comments')
def api_comments():
    page = request.form.get('page', 1)
    p = Comment.query.order_by(
        Comment.created_at.desc()).paginate(page=page,per_page=10)
    comments = p.items
    for b in range(len(comments)):
        comments[b] = comments[b].to_dict()
        comments[b]['created_at'] = [
            comments[b]['created_at'], datetime_filter(
                comments[b]['created_at'])]
    return dict(page={'page': p.page,
            'per_page':p.per_page,
            'total': p.total,
            'pages':p.pages,
            'first':p.first,
            'last':p.last,
            'has_prev':p.has_prev,
            'prev_num':p.prev_num,
            'has_next':p.has_next,
            'next_num':p.next_num}, comments=comments)

@app.route('/api/blogs/<id>/comments', methods=['POST'])
def api_create_comment(id):
    user = get_user()
    content = request.form.get('content', None)
    if user is None:
        return APIPermissionError('Please sign in first.')
    if not content or not content.strip():
        return APIValueError('content')
    blog = Blog.query.filter(Blog.id == id).one()
    if blog is None:
        return APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, 
    user_name=user.name, user_image=user.image,
                      content=content.strip())
    db.session.add(comment)
    db.session.commit()
    return comment.to_dict()
