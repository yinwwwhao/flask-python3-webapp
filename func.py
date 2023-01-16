from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from flask import request, redirect, abort
from models import User, Blog
import smtplib
import time
import hashlib
from configs import smtp_server, from_addr, password


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

    
    to_addr = email
    

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
    elif user.admin != True:
        return abort(403)
    else:
        return ''


def get_user():
    try:
        cookie_str = request.cookies[COOKIE_NAME]
        user = cookie2user(cookie_str)
        if user:
            u = user.to_dict()
            u.passwd = '******'
            return u
        else:
            return None
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


def text2html(text):
    lines = map(lambda s: '%s' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)
