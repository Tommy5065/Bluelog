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