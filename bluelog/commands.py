import click
from bluelog.extions import db
def register_command(app):
    @app.cli.command()
    @click.option('--category', default=10, help='generate fake category')
    @click.option('--text', default=50, help='generate fake text')
    @click.option('--comment', default=100, help='generate fake comment')
    def forge(category, text, comment):
        """generate data"""

        db.drop_all()
        db.create_all()
        click.echo('OK')

        from fakers import faker_admin, faker_category, faker_comment,faker_text

        click.echo('Working admin')
        faker_admin()

        click.echo(f"Working {category} category")
        faker_category(category)

        click.echo(f"Working {text} text")
        faker_text(text)

        click.echo(f"Working {comment} comment")
        faker_comment(comment)

        click.echo('Done')



    @app.cli.command()
    @click.option('--username', prompt=True, help='generate admin name')
    @click.password_option()
    def init(username,password):
        """Generate admin count"""
        db.drop_all()
        db.create_all()

        from bluelog.models import Admin
        admin = Admin.query.first()
        if admin:
            click.echo('Admin count has already been, update the information')
            admin.adminName = username
            admin.generate_hash(password)
            click.echo('update finish')
        else:
            click.echo('generate a new count')
            admin = Admin(
                adminName=username,
                name = 'Yeri',
                blog_title='BlueLog',
                blog_sub_title = 'No, I am a real thing',
                about='Any thing about you'
            )
            admin.generate_hash(password)
            db.session.add(admin)

        from bluelog.models import Category
        category = Category.query.first()
        if category is None:
            click.echo('Generate a default category')
            category = Category(name='default')
            db.session.add(category)
        else:
            click.echo('categories has exist')

        db.session.commit()
        click.echo('Done!')