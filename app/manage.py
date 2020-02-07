import unittest
import coverage
import random
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from web import create_app, db, socket_io
from web.models import User, Message
from faker import Faker

fake = Faker()

app = create_app()

COV = coverage.coverage(
    branch=True,
    include='web/*'
)
COV.start()

Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def drop():
    db.drop_all()


@manager.command
def seed():
    db.session.query(Message).delete()
    db.session.query(User).delete()
    db.session.commit()

    for x in range(1, 60):
        user = User(
            username=fake.name(),
            email='test{}@test.com'.format(x),
            confirmed=True
        )
        user.set_password('test')
        db.session.add(user)

    users_id = db.session.query(User.id).all()

    for _ in range(5):
        for first_user in users_id:
            for second_user in users_id:
                message = Message(
                    user_from_id=first_user[0],
                    user_to_id=second_user[0],
                    text=fake.text()[:127]
                )
                db.session.add(message)
    db.session.commit()




def run_tests():
    test = unittest.TestLoader().discover(start_dir='tests', pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(test)
    return result


def report():
    result = run_tests()
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    else:
        return 1


@manager.command
def tests(option):
    if option == 'report':
        report()
    elif option == 'all':
        run_tests()
    else:
        print('invalid arguments')


@manager.command
def run():
    socket_io.run(app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
