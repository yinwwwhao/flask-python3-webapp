'''
为了这个东西的可持续发展，我觉得以单文件运行过于难以维护
所以就放弃了这个文件
留个纪念
'''
from apis import APIValueError, APIPermissionError, APIError, Page, APIResourceNotFoundError
from datetime import datetime
from models import User, Blog, Comment, db, next_id, Atlas
from flask import Flask, request, make_response, render_template, redirect, abort, session
import re
import hashlib
from sqlalchemy.sql import func
import time
import sql_configs
import markdown
import os
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import random
import smtplib
import base64
from log import logging

app = Flask(__name__)
app.config.from_object(sql_configs)
db.init_app(app)

COOKIE_NAME = 'awesession'
_COOKIE_KEY = 'Awesome'



def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


def send_email(verification, email):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = 'ywh1357zqsl@163.com'
    password = 'AESOBKBQUBFALUJQ'
    to_addr = email
    smtp_server = 'smtp.163.com'

    msg = MIMEText(f'您的邮箱验证码为：\n{verification}', 'plain', 'utf-8')
    msg['From'] = _format_addr('尹伟豪 <%s>' % from_addr)
    msg['To'] = _format_addr('尊敬的用户 <%s>' % to_addr)
    msg['Subject'] = Header('邮箱验证码', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except BaseException:
        pass
    if p < 1:
        p = 1
    return p


def user2cookie(user):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-sha1
    s = '%s-%s' % (user.id, _COOKIE_KEY)
    L = [user.id, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


def cookie2user(cookie_str):
    """
    Parse cookie and load user if cookie is valid.
    """
    if not cookie_str:
        return

    L = cookie_str.split('-')
    if len(L) != 2:
        return
    uid, sha1 = L
    user = User.query.filter(User.id == uid).one()
    if user is None:
        return
    s = '%s-%s' % (uid, _COOKIE_KEY)
    if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
        return
    return user


def check_admin():
    user = get_user()
    if not user:
        return redirect('/signin')
    if user.admin != True:
        return abort(403)


def get_user():
    try:
        cookie_str = request.cookies[COOKIE_NAME]
        user = cookie2user(cookie_str)
        u = user.to_dict()
        u.passwd = '******'
        return u
    except BaseException:
        return None


def bubbleSort(arr):
    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):
            if arr[j]['int'] < arr[j + 1]['int']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def get_tag():
    t = []
    for blog in Blog.query.all():
        t.append(blog.tag)
    tags = []
    for tag in t:
        if {'int': t.count(tag), 'name': tag} in tags:
            continue
        tags.append({'int': t.count(tag), 'name': tag})

    return bubbleSort(tags)


@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    if request.args.get('tag', None):
        num = db.session.query(func.count(Blog.id)).scalar()
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
        num = db.session.query(func.count(Blog.id)).scalar()
        p = Page(num, page_size=5, page_index=page)
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


@app.route('/atlas/public')
def atlas():
    page = int(request.args.get('page', 1))
    user = get_user()
    num = db.session.query(func.count(Atlas.name)).filter(
        False == Atlas.private).scalar()
    p = Page(num, page_size=20, page_index=page)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self().order_by(Atlas.created_at.desc()).filter(Atlas.private == False).all()
    return render_template('atlas.html', user=user, image=image, page=p)


@app.route('/atlas')
def atlas_redirect():
    return redirect('/atlas/public')


@app.route('/atlas/private')
def atlas_private():
    user = get_user()
    if not user:
        pass
    elif user.admin != True:
        return abort(403)
    else:
        pass
    page = int(request.args.get('page', 1))
    user = get_user()
    num = db.session.query(func.count(Atlas.name)).filter(
        True == Atlas.private).scalar()
    p = Page(num, page_size=20, page_index=page)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self().order_by(Atlas.created_at.desc()).filter(Atlas.private == True).all()
    return render_template('atlas_private.html', user=user, image=image, page=p)


@app.route('/about')
def about():
    return render_template('about.html', user=get_user())




@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signout')
def signout():
    r = make_response("<script>location.assign('/');</script>")
    r.delete_cookie(COOKIE_NAME)
    return r


@app.route('/get_verification', methods=['post'])
def get_verification():
    return str(session.get(request.form.get('email')))


@app.route('/send_verification', methods=['post'])
def send_verification():
    verification = random.randint(0, 999999)
    session[request.form.get('email')] = verification
    send_email(verification, request.form.get('email'))
    return 'send ok'


@app.route('/api/authenticate', methods=['post'])
def authenticate():
    email = request.form['email']
    passwd = request.form['passwd']
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')

    users = User.query.filter(User.email == email).all()
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]

    sha1 = hashlib.sha1(
        user.email.encode('utf-8') +
        b':' +
        passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')

    # authenticate ok, set cookie:
    r = make_response()
    r.set_cookie(
        COOKIE_NAME,
        user2cookie(user),
        httponly=True)

    return r


_RE_EMAIL = re.compile(
    r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


@app.route('/api/users', methods=['get', 'post'])
def user():
    if request.method == 'POST':

        email = request.form['email']
        name = request.form['name']
        passwd = request.form['passwd']

        if not name or not name.strip():
            raise APIValueError('name')
        if not email or not _RE_EMAIL.match(email):
            raise APIValueError('email')
        if not passwd or not _RE_SHA1.match(passwd):
            raise APIValueError('passwd')
        users = User.query.filter(User.email == email).all()
        if len(users) > 0:
            raise APIError(
                'register:failed',
                'email',
                'Email is already in use.')
        uid = next_id()
        new_user = User(id=uid, name=name.strip(), email=email,
                        passwd=passwd,
                        image='/static/images/user.svg',
                        admin=True)
        db.session.add(new_user)
        db.session.commit()

        del session[request.form.get('email')]
        # make session cookie:
        r = make_response("<script>location.assign('/');</script>")
        r.set_cookie(COOKIE_NAME, user2cookie(
            new_user), httponly=True)
        return r
    else:
        users = User.query.order_by(User.created_at.desc()).all()
        for u, i in zip(users, range(len(users))):

            users[i] = u.to_dict()
            u.passwd = '******'
            users[i]['created_at'] = [
                users[i]['created_at'], datetime_filter(
                    users[i]['created_at'])]
        return dict(users=users)


def text2html(text):
    lines = map(lambda s: '%s' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


@app.route('/manage/')
def manage():
    return redirect('/manage/comments')


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


@app.route('/manage/comments')
def manage_comment():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(func.count(Comment.id)).scalar()
    p = Page(num, page_size=10)

    return render_template('manage_comments.html',
                           page_index=get_page_index(page),
                           page=p,
                           user=get_user())


@app.route('/api/blogs/<id>/delete', methods=['POST'])
def delete_blog(id):
    if check_admin():
        return check_admin()
    Blog.query.filter(Blog.id == id).delete()
    Comment.query.filter(Comment.blog_id == id).delete()
    db.session.commit()
    return 'delete ok'


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
    num = db.session.query(func.count(Blog.id)).scalar()
    p = Page(num, page_size=5)
    return render_template('manage_blogs.html',
                           page_index=get_page_index(page),
                           page=p,
                           user=get_user())


@app.route('/api/comments/<id>/delete', methods=['POST'])
def delete_comment(id):
    if check_admin():
        return check_admin()
    Comment.query.filter(Comment.id == id).delete()
    db.session.commit()
    return 'delete ok'


@app.route('/api/atlas/delete', methods=['POST'])
def delete_atlas():
    if check_admin():
        return check_admin()
    url = request.form.get('url')
    if not url or not url.strip():
        raise APIValueError('url')
    Atlas.query.filter(Atlas.url == url).delete()
    db.session.commit()
    os.remove(os.path.join(*url[1:].split('/')))
    return 'delete ok'


@app.route('/manage/users')
def manage_user():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(func.count(User.id)).scalar()
    p = Page(num, page_size=5)
    return render_template('manage_users.html',
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


@app.route('/manage/atlas')
def manage_atlas():
    if check_admin():
        return check_admin()
    page = request.args.get('page', 1)
    num = db.session.query(func.count(Atlas.url)).scalar()
    p = Page(num, page_index=page, page_size=20)
    image = Atlas.query.offset(
        p.offset).limit(
        p.limit).from_self(
    ).order_by(
            Atlas.created_at.desc()).all()
    return render_template('manage_atlas.html', 
                page=p, 
                image=image,
                user=get_user())


@app.route('/api/blogs/<id>')
def api_get_blog(id):
    blog = Blog.query.filter(Blog.id == id).one().to_dict()
    return blog


@app.route('/api/comments')
def api_comments():
    page = request.form.get('page', 1)
    page_index = get_page_index(page)
    num = db.session.query(func.count(Blog.id)).scalar()
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


@app.route('/api/atlas', methods=['POST'])
def api_create_atlas():
    if check_admin():
        return check_admin()

    data = request.form.get('data')
    name = request.form.get('name')
    private = request.form.get('private')
    if private == 'false':
        private = False
    else:
        private = True
    filetype = request.form.get('filetype')
    if not data or not data.strip():
        raise APIValueError('data')
    if not name or not name.strip():
        raise APIValueError('name')
    if not filetype or not filetype.strip():
        raise APIValueError('filetype')

    for x in os.listdir('static/images'):
        if os.path.isfile(x):
            if x.split('.')[-1] != filetype:
                os.rename(f'static/images/{x}', 'static/images/{}'.format(
                '.'.join(x.split('.')[:-1])+'.'+filetype))
    data = base64.b64decode(data)
    with open('static/images/{0}.{1}'.format(name, filetype), 'wb') as f:
        f.write(data)

    if not Atlas.query.filter(Atlas.name == name).all():
        image = Atlas(
            name=name, url='/static/images/{0}.{1}'.format(name, filetype), private=private)
        db.session.add(image)
        db.session.commit()
    else:
        Atlas.query.filter(Atlas.name == name).update({
            'name': name,
            'url': '/static/images/{0}.{1}'.format(name, filetype),
            'private': private,
            'created_at': time.time()
        })
        db.session.commit()
    return 'create or update atlas ok'

@app.route('/api/atlas/rename', methods=['POST'])
def rename_atlas():
    name = request.form.get('name')
    newname = request.form.get('newname')
    if not name or not newname:
        raise APIValueError('name')
    
    
    for x in os.listdir('static/images'):
        print('.'.join(x.split('.')[:-1])*10000000)
        if '.'.join(x.split('.')[:-1]) == newname:
            t = x.split('.')[-1]
            os.rename(x, newname + '.' + x.split('.')[-1])
    Atlas.query.filter(Atlas.name == name).update({
        'name': newname,
        'created_at': time.time(),
        'url': f'/static/images/{newname}.{t}'
    })
    db.session.commit()
    return 'rename ok'



@app.route('/api/atlas/private', methods=['POST'])
def private_atlas():
    private = request.form.get('private')
    name = request.form.get('name')
    if private == 'false':
        private = False
    else:
        private = True
    Atlas.query.filter(Atlas.name == name).update({
        'private': private
    })
    db.session.commit()
    return 'update ok'


@app.route('/api/blogs', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        if check_admin():
            return check_admin()
        user = get_user()
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
        num = db.session.query(func.count(Blog.id)).scalar()
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


app.add_template_filter(datetime_filter, 'datetime')

if __name__ == '__main__':
    logging.info('Server started.')
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
