from flask import Blueprint, render_template, request, current_app
from flask_login import login_required

from bluelog.helpers import redirect_up
from bluelog.models import Post
from bluelog.extions import db
bp = Blueprint('admin',__name__)



@bp.before_request
@login_required
def login_protect():
    pass

@bp.route('/write')
def new_post():
    return render_template('admin/write.html')

@bp.route('/category')
def new_category():
    return render_template('admin/create_category.html')

@bp.route('/setting')
def setting():
    return render_template('admin/setting.html')

@bp.route('/manage/post')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/Manage_Post.html', posts=posts, pagination=pagination)

@bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect_up()
