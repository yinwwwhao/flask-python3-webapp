from app import app
from func import check_admin, get_user, get_page_index
from flask import render_template, request
from models import Blog, db
from apis import Page
from sqlalchemy.sql import func as sqlfunc
from log import logging

logging.info('manager/blog.py started.')

@app.route('/manage/blogs/create')
def create_blog():
    if check_admin():
        return check_admin()
    return render_template('manage_blog_edit.html', 
    id='', 
    action='/api/blogs', 
    user=get_user(), 
    title='创建')


@app.route('/manage/blogs')
def manage_blog():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(sqlfunc.count(Blog.id)).scalar()
    p = Page(num, page_size=8)
    return render_template('manage_blogs.html',
                           page_index=get_page_index(page),
                           page=p,
                           user=get_user())




@app.route('/manage/blogs/edit')
def edit_blog():
    if check_admin():
        return check_admin()
    id = request.args.get('id')
    blog = Blog.query.filter(Blog.id == id).one().to_dict()
    return render_template('manage_blog_edit.html',
                           id=blog.id, action='/api/blogs', user=get_user(), title='编辑')
