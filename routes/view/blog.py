from app import app
from models import Blog, Comment
import markdown
from flask import render_template
from func import get_user, text2html
from log import logging

logging.info('view/blog.py started.')

@app.route('/blogs/<id>')
def get_blog(id):
    blog = Blog.query.filter(Blog.id == id).one().to_dict()
    comments = Comment.query.filter(
        Comment.blog_id == id).order_by(
        Comment.created_at.desc()).all()
    blog.content = markdown.markdown(blog.content)
    for x, y in zip(comments, range(len(comments))):
        comments[y] = x.to_dict()
        comments[y].content = markdown.markdown(text2html(comments[y].content))
    return render_template('blog.html', blog=blog,
                           comments=comments, user=get_user())

