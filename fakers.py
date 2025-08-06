import random
from bluelog.models import Post, Comment, Category, Admin
from bluelog.extions import db
from faker import Faker

def faker_admin():
    admin = Admin(
        adminName = 'admin',
        name = 'Erick',
        blog_title = 'Bluelog',
        blog_sub_title = "No, I am a real thing",
        about = 'I am initialising about page'
    )
    admin.generate_hash('hello, flask')
    db.session.add(admin)
    db.session.commit()

faker = Faker('')

def faker_category(count=10):
    category = Category(name='default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=faker.unique.name())
        db.session.add(category)
        try:
            db.session.commit()
        except InterruptedError:
            db.session.rollback()

def faker_text(count=50):
    for i in range(count):
        text = Post(
            title = faker.sentence(),
            body = faker.text(2000),
            category = Category.query.get(random.randint(1,Category.query.count())),
            timestamp = faker.date_time_this_year()
        )
        db.session.add(text)
    db.session.commit()

def faker_comment(count=100):
    for i in range(count):
        comment = Comment(
            name = faker.name(),
            email = faker.email(),
            site = faker.url(),
            body = faker.sentence(),
            review = True,
            timestamp = faker.date_time_this_year(),
            post = Post.query.get(random.randint(1,Post.query.count()))
    )
        db.session.add(comment)

    salt = int(count * 0.1)
    # 未过审评论
    for i in range(salt):
        comment1 = Comment(
            name=faker.name(),
            email=faker.email(),
            body=faker.sentence(),
            site=faker.url(),
            review=False,
            timestamp=faker.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment1)
    # 管理员发表评论
    for i in range(salt):
        comment2 = Comment(
            name = 'Eric',
            email = '2194927699@qq.com',
            body = faker.sentence(),
            site=faker.url(),
            from_admin = True,
            review = True,
            timestamp = faker.date_time_this_year(),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment2)
    # 评论回复
    for i in range(salt):
        comment3 = Comment(
            name = faker.name(),
            email = faker.email(),
            body = faker.sentence(),
            site=faker.url(),
            review = True,
            timestamp = faker.date_time_this_year(),
            replied = Comment.query.get(random.randint(1,Comment.query.count())),
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment3)
    db.session.commit()
