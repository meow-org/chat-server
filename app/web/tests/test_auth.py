import os
import unittest
from web import app

TEST_DB = 'test.db'


class APITest(unittest.TestCase):
    def setUp(self):
        # app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        # app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #                                         os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
        #
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)
        pass

    # executed after each test
    def tearDown(self):
        pass

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
