from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, abort, make_response
from flask_login import current_user


from bluelog.models import Post, Comment, Category
from bluelog.helpers import is_url_safe, redirect_up
from bluelog.forms import AdminForm, CommentForm
from bluelog.extions import db
from bluelog.emails import send_new_comments,send_comments_reply
bp = Blueprint('blog', __name__)

@bp.route('/', defaults={'page':1})
@bp.route('/page/<int:page>')
def index(page):
    # 分页处理使用pagination函数：1.知道当前位于那一页(page)，2.总共要分成多少页(per_page)，3.正常呈现每一页的数量(对象属性item)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)

@bp.route('/about')
def about():
    return render_template('blog/about.html')

@bp.route('/category/<int:category_id>')
def show_category(category_id):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_url_safe(target):
            category = Category.query.get_or_404(category_id)
            page = request.args.get('page', type=int)
            per_page = current_app.config['BLUELOG_POST_PER_PAGE']
            pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
            posts = pagination.items
            return render_template('blog/category.html',posts=posts, pagination=pagination,category=category)
    return render_template('blog/category.html')

@bp.route('/show_post/<int:post_id>', methods=['Get', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page',type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page=page,per_page=per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminForm()
        form.auth.data = current_user.name
        form.email.data = current_app.config['MAIL_USERNAME']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        name = form.auth.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(name=name, email=email, site=site, body=body,from_admin=from_admin, review=reviewed)

        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_comments_reply(replied_comment)
            flash('Thanks your reply has been send to author', 'info')
        db.session.add(comment)
        db.session.commit()

        flash('Thanks your comments will be published after reviewed', 'info')
        send_new_comments(post)
        return redirect(url_for('.show_post',post_id=post.id))

    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination,form=form)

@bp.route('/reply/comment/<int:comment_id>', methods=['POST','GET'])
def reply_comment(comment_id):
        comment = Comment.query.get_or_404(comment_id)
        return redirect(url_for('.show_post',post_id=comment.post_id, reply=comment.id_, auth=comment.name)+"#comment-form")

@bp.route('/change_theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_up())
    response.set_cookie('theme',theme_name,max_age=30*24*60*60)
    return response