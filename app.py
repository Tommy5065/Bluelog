import os
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from bluelog.settings import Config
from bluelog.extions import bootstrap, ckeditor, db, moment,login, csrf_protect
from bluelog.commands import register_command
from bluelog.models import Admin, Category, Comment

from blueprint.blog import bp as blog_bp
from blueprint.admin import bp as admin_bp
from blueprint.auth import auth_bp

def create_app(config_name=None):

    app = Flask(__name__)


    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app.config.from_object(Config[config_name])

    def register_extensions(app):
        bootstrap.init_app(app)
        ckeditor.init_app(app)
        db.init_app(app)
        moment.init_app(app)
        login.init_app(app)
        csrf_protect.init_app(app)

    def register_errors(app):
        @app.errorhandler(CSRFError)
        def bad_request(e):
            return render_template('error/400.html', description=e.description),400

    def register_template_context(app):
        @app.context_processor
        def template_context():
            admin = Admin.query.first()
            categories = Category.query.order_by(Category.name).all()
            if current_user.is_authenticated:
                unread_comments = Comment.query.filter_by(review=False).count()
            else:
                unread_comments = None
            return dict(admin=admin, categories=categories, unread_comments=unread_comments)

    def register_blueprint(app):
        app.register_blueprint(blog_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp,url_prefix='/auth')

    register_extensions(app)
    register_command(app)
    register_errors(app)
    register_template_context(app)
    register_blueprint(app)

    login.login_view = 'auth.login'
    login.login_message_category = 'warning'

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run()

