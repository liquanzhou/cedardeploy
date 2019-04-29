#!/usr/bin/env python
# coding: utf-8
# python manager.py runserver
# python manager.py runserver  -d -r -h 10.172.159.74 -p 5000

# python manager.py db init
# python manager.py db migrate
# python manager.py db upgrade
# python manager.py shell
# with app.app_context():
#     u = User(email='admin@163.com',username='admin',password='admin')
#     db.session.add(u)
#     db.session.commit()

from app import create_app, db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
