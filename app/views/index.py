from app.views import views_blueprint as app
from flask import request, render_template
from app.models import Blog
from func import get_user

def get_tag():
    t = []
    for blog in Blog.query.all():
        t.append(blog.tag)
    tags = []
    for tag in t:
        if {'int': t.count(tag), 'name': tag} in tags:
            continue
        tags.append({'int': t.count(tag), 'name': tag})

    return sorted(tags, key=lambda x:x.get('int'), reverse=True)

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    if request.args.get('tag', None):
        p = Blog.query.filter(
            Blog.tag == request.args.get('tag', None)
        ).order_by(
            Blog.created_at.desc()).paginate(page=page, per_page=5)
        blogs = p.items
        user = get_user()
        return render_template('index.html', blogs=blogs, user=user, title=request.args.get('tag', None), tags=get_tag(), page=p, tag=request.args.get('tag', None))
    else:
        user = get_user()
        p = Blog.query.order_by(
            Blog.created_at.desc()).paginate(page=page,per_page=5)
        blogs = p.items
        return render_template('index.html',
                               user=user,
                               blogs=blogs,
                               title='首页',
                               tags=get_tag(),
                               page=p)