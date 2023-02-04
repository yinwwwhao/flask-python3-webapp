from app.views import views_blueprint as app
from flask import request, render_template, redirect, abort
from func import get_user
from app.models import Atlas
from log import logging

logging.info('view/atlas started.')

@app.route('/atlas/public')
def atlas():
    page = int(request.args.get('page', 1))
    user = get_user()
    p = Atlas.query.order_by(Atlas.created_at.desc()).filter(Atlas.private == False).paginate(page=page, per_page=10)
    image = p.items
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
    p = Atlas.query.order_by(Atlas.created_at.desc()).filter(Atlas.private == True).paginate(page=page, per_page=10)
    image = p.items
    return render_template('atlas_private.html', user=user, image=image, page=p)
