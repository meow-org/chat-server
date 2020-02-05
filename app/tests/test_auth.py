import os
import unittest
import json
from web import create_app, db, mail
from web.config import TestConf, AUTH_URL_PREFIX
from web.models import User


class APITest(unittest.TestCase):
    def setUp(self):
        app = create_app(TestConf)
        self.app = app.test_client()
        self.mail = mail
        db.session.close()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def register(self, **kwargs):
        return self.app.post(
            AUTH_URL_PREFIX + '/registration',
            data=json.dumps(kwargs),
            content_type="application/json"
        )

    def json_message_equal(self, response, message):
        self.assertEqual(json.loads(response.data)['message'], message)

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_registration_input(self):
        # Test required params
        response = self.register()
        self.assertEqual(response.status_code, 400)
        self.json_message_equal(response, "'email' is a required property")
        response = self.register(username='test')
        self.json_message_equal(response, "'email' is a required property")
        response = self.register(username='test', email='test@test.com')
        self.json_message_equal(response, "'password' is a required property")
        # Test email address
        response = self.register(username='test', email='test@test', password='123456')
        self.json_message_equal(response, "Wrong email address")
        # Password must between 3 and 32 characters
        response = self.register(username='test', email='test@test.ru', password='12')
        self.json_message_equal(response, "Your password too short")
        response = self.register(username='test', email='test@test.ru',
                                 password='1234567890123456789012345678901234567890')
        self.json_message_equal(response, "Your password too long")

    def test_registration(self):
        with self.mail.record_messages() as outbox:
            response = self.register(username='test', email='test@test.ru', password='1234')
            self.assertEqual(outbox[0].subject, 'test')
            self.assertEqual(outbox[0].recipients[0], 'test@test.ru')
            user = User.query.all()[0]
            print('t', user)
            self.assertEqual(user.email, 'test@test.ru')
            self.assertEqual(user.username, 'test')
            self.assertEqual(user.confirmed, False)
            self.assertIsNotNone(user.email_token)


if __name__ == '__main__':
    unittest.main()
