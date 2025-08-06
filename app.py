import os
from flask import Flask, render_template
from bluelog.settings import Config
from bluelog.extions import bootstrap, ckeditor, db, moment,login
from bluelog.commands import register_command
from bluelog.models import Admin, Category
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

    def register_errors(app):
        @app.errorhandler(400)
        def bad_request(e):
            return render_template('error/400.html'),400

    def register_template_context(app):
        @app.context_processor
        def template_context():
            admin = Admin.query.first()
            categories = Category.query.order_by(Category.name).all()
            return dict(admin=admin, categories=categories)

    def register_blueprint(app):
        app.register_blueprint(blog_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp)

    register_extensions(app)
    register_command(app)
    register_errors(app)
    register_template_context(app)
    register_blueprint(app)
    @app.route('/')
    def hello_world():  # put application's code here
        return '这是在工厂函数里注册的路由!'

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run()

