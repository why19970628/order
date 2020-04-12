from application import app, manager, db
from application import app, manager
from flask_script import Server
from jobs.launcher import runjob
from flask_migrate import Migrate, MigrateCommand
import www


# database migrate comand
"""
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
"""
Migrate(app, db)
manager.add_command('db', MigrateCommand)


# web server
manager.add_command('runserver', Server(
    # host='0.0.0.0',
    port=app.config['SERVER_PORT'],
    use_debugger=True
))
# job entrance
manager.add_command('runjob', runjob())


def main():
    manager.run()


if __name__ == '__main__':
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()  # 打印错误


