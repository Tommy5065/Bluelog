from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditorField, CKEditor
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


bootstrap = Bootstrap4()
ckeditor = CKEditor()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
