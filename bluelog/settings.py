import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = (MAIL_USERNAME)

    BLUELOG_USERNAME = os.getenv('BLUELOG_USERNAME')
    BLUELOG_POST_PER_PAGE = 5
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 25
    BLUELOG_THEMES = {'perfect_blue':'Perfect Blue', 'black_swan':'Black Swan'}

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.db')

class TestingConfig(BaseConfig):
    TestingConfig = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite' + os.path.join(basedir,'data.db'))


Config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig

}