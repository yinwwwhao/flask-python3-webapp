from app.manage import manage_blueprint as app
from func import check_admin, get_user
from flask import render_template
from app.models import Blog
from log import logging

logging.info('manager/blog.py started.')

@app.route('/manage/blogs/create')
def create_blog():
    admin = check_admin()
    if admin:
        return admin
    return render_template('manage/manage_blog_edit.html', 
    user=get_user(), 
    title='创建')


@app.route('/manage/blogs')
def manage_blog():
    admin = check_admin()
    if admin:
        return admin
    return render_template('manage/manage_blogs.html',
                           user=get_user())




@app.route('/manage/blogs/edit')
def edit_blog():
    admin = check_admin()
    if admin:
        return admin
    return render_template('manage/manage_blog_edit.html', user=get_user(), title='编辑')
