from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditorField, CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


bootstrap = Bootstrap4()
ckeditor = CKEditor()
db = SQLAlchemy()
moment = Moment()
login = LoginManager()
csrf_protect = CSRFProtect()

# 设置回调函数，使用flask-login验证用户登录状态时不仅返回用户id，而是返回用户模型类对象
@login.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    admin = Admin.query.get(int(user_id))
    return admin
