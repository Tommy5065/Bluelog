from bluelog.extions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(20))
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(25))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    about = db.Column(db.Text)
    def generate_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password_hash(self, password):
        return check_password_hash(self.password_hash, password)




class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.relationship('Comment', back_populates='post', cascade='all')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='post')
    can_comments = db.Column(db.Boolean, default=True)

class Comment(db.Model):
    __tablename__ = 'comment'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120))
    site = db.Column(db.String(255), nullable=True)
    body = db.Column(db.String(120), nullable=False)
    from_admin = db.Column(db.Boolean, default=False) # 是否是管理员发布的评论
    review = db.Column(db.Boolean, default=False) # 是个通过后台审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship(Post,back_populates='comment')

     # 邻接列表关系: 设置评论回复
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id_'))
    replied = db.relationship("Comment", back_populates='replies', remote_side=[id_]) # 被回复的父评论
    replies = db.relationship("Comment", back_populates='replied', cascade='all')




class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post = db.relationship(Post, back_populates='category')

    # 删除分类后文章划为默认分类
    def Delete(self):
        default_category = Category.query.get(1)
        posts = self.post[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()