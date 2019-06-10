import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import inspect

students_db = SQLAlchemy()


def init_app(app):
    students_db.init_app(app)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    students_db.create_all()
    click.echo('Initialized the database.')


class Student(students_db.Model):
    id = students_db.Column(students_db.Integer, primary_key=True)
    fname = students_db.Column(students_db.String(60), nullable=False)
    lname = students_db.Column(students_db.String(60), nullable=False)
    agegrup = students_db.Column(students_db.Integer, nullable=False)
    specialization = students_db.Column(students_db.String(120),
                                        nullable=False)

    def update_with(self, update_dict):
        self.fname = update_dict['fname']
        self.lname = update_dict['lname']
        self.agegrup = update_dict['agegrup']
        self.specialization = update_dict['specialization']


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
