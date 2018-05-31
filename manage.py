import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import db
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager()
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context()))


if __name__ == '__main__':
    app.run()
