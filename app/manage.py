import unittest
import coverage
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from web import app, db
from web.models import User, Message
from faker import Faker

fake = Faker()

COV = coverage.coverage(
    branch=True,
    include='web'
)
COV.start()

Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    try:
        db.session.query(Message).delete()
        db.session.query(User).delete()
        db.session.commit()

        for x in range(1, 20):
            user = User(
                username=fake.name(),
                email='test{}@test.com'.format(x),
                confirmed=True
            )
            user.set_password('test')
            db.session.add(user)

        users_id = db.session.query(User.id).all()

        for _ in range(5):
            for dt in users_id:
                message = Message(
                    user_id=dt[0],
                    text=fake.text()[:127]
                )
                db.session.add(message)
    except:
        db.session.rollback()
    db.session.commit()


@manager.command
def test():
    tests = unittest.TestLoader().discover(start_dir='web', pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
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
def run():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
