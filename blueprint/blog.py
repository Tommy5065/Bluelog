from flask import Blueprint,render_template,request,current_app
from bluelog.models import Post, Comment
from bluelog.helpers import is_url_safe

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
            return render_template('blog/category.html')
    return render_template('blog/category.html')

@bp.route('/show_post/<int:post_id>', methods=['Get', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page',type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page=page,per_page=per_page)
    comments = pagination.items
    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination)