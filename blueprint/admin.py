from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required

from bluelog.helpers import redirect_up
from bluelog.models import Post, Category, Comment
from bluelog.extions import db
from bluelog.forms import PostForm, CategoryForm
bp = Blueprint('admin',__name__)



@bp.before_request
@login_required
def login_protect():
    pass

@bp.route('/write', methods=['GET','Post'])
def new_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
        title = post_form.title.data
        body = post_form.body.data
        category = Category.query.get_or_404(post_form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Create Post successfully','success')
        return redirect(url_for('blog.show_post', post_id=post.id))

    return render_template('admin/write.html', form=post_form)


@bp.route('/create_category', methods=['POST','GET'])
def new_category():
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        category = Category.query.get(form.name.data)
        if category:
            flash('Name already in use.','warning')
            return redirect_up()

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Create Category Successfully', 'success')
        return redirect(url_for('blog.show_category', category_id=category.id))

    return render_template('admin/create_category.html', form=form)

@bp.route('/manage/category', methods=['GET', 'POST'])
def manage_category():
    page = request.args.get('page',1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Category.query.order_by(Category.timestamp.asc()).paginate(page=page, per_page=per_page)
    categories = pagination.items
    return render_template('admin/Manage_Category.html', categories=categories, pagination=pagination)

@bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category_id == 1:
        flash('Can not delete default kind','warning')
        return redirect_up()
    category.Delete()
    flash('Delete Category Successfully','success')
    return redirect_up()

@bp.route('/edit_category/<int:category_id>', methods=['POST','GET'])
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get(category_id)

    if form.validate_on_submit():
        name = form.name.data
        category.name=name
        db.session.commit()
        flash('Edit Category Name Successfully','success')
        return redirect(url_for('.manage_category'))
    form.name.data =category.name
    return render_template('admin/create_category.html', form=form)

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

@bp.route('/edite_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post_form = PostForm()
    post = Post.query.get_or_404(post_id)

    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.body = post_form.body.data
        post.category = Category.query.get_or_404(post_form.category.data)
        db.session.commit()
        flash('Post update', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    post_form.title.data = post.title
    post_form.category.data = post.category_id
    post_form.body.data = post.body

    return render_template('admin/write.html', form=post_form)


@bp.route('/manage/comments')
def manage_comments():
    request_filter = request.args.get('filter','all')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if request_filter == 'Unread':
        filter_comments = Comment.query.filter_by(review=False)
    elif request_filter == 'from_admin':
        filter_comments = Comment.query.filter_by(from_admin=True)
    else:
        filter_comments = Comment.query

    pagination = filter_comments.order_by(Comment.timestamp.desc()).paginate(page=page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/Manage_Comments.html', comments=comments, pagination=pagination)

@bp.route('/approve/<int:comment_id>')
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.review=True
    db.session.commit()
    flash('Comment published','success')
    return redirect_up()

@bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect_up()

@bp.route('/comment_button/<int:post_id>',methods=['POST'])
def comment_button(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comments:
        post.can_comments=False
        db.session.commit()
        flash('Comment close','info')
    else:
        post.can_comments=True
        db.session.commit()
        flash('Comment open','success')
    return redirect_up()

