from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, length, email, optional, url

# 创建登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(1,20)])
    password = PasswordField('Password', validators=[DataRequired(), length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login in')

# 创建文章表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(1,60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # 设置SelectField下拉选项（option）的值由choices设置
    def __init__(self, *args, **kwargs):
        from bluelog.models import Category
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


# 创建分类表单
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(1,30)])
    submit = SubmitField('Submit')

    # 防止分类名称重复自定义验证器
    def validate_name(self, field):
        from bluelog.models import Category
        if Category.query.filter_by(name=field.date).first():
            raise ValueError('Name already in use.')

#创建评论表单
class CommentForm(FlaskForm):
    auth = StringField('Name', validators=[DataRequired(), length(1,30)])
    email = StringField('Email', validators=[DataRequired(), email(), length(1,254)])
    site = StringField('Site', validators=[optional(), url(), length(0,255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()

# 为管理员设置个评论表单
class AdminForm(CommentForm):
    auth = HiddenField()
    email = HiddenField()
    site = HiddenField()