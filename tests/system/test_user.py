""""
System Tests: be sure to start the Docker container before you run these APIs tests
"""

import json

from lookup_tables.messages import MessageCode
from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):

    def test_register_user(self):
        with self.app() as c:
            with self.app_context():
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})

                self.assertEqual(register_request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_email('john.doe@email.com'))

    def test_register_and_login_successful(self):
        with self.app() as c:
            with self.app_context():
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})
                self.assertEqual(register_request.status_code, 201)
                login_request = c.post('/v1/login', json={'email': 'john.doe@email.com',
                                                          'password': 'password'},
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(login_request.status_code, 200)
                self.assertIn('access_token', json.loads(login_request.data).keys())
                self.assertIn('refresh_token', json.loads(login_request.data).keys())

    def test_register_and_login_failed(self):
        with self.app() as c:
            with self.app_context():
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})
                self.assertEqual(register_request.status_code, 201)
                login_request = c.post('/v1/login', json={'email': 'john.doe@email.com',
                                                          'password': 'wrong-password'},
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(login_request.status_code, 401)
                self.assertEqual(json.loads(login_request.data).get('message'), MessageCode.INVALID_CREDENTIALS)

    def test_register_duplicate_user(self):
        with self.app() as c:
            with self.app_context():
                c.post('/v1/register', json={'email': 'john.doe@email.com',
                                             'name': 'John',
                                             'surname': 'Doe',
                                             'password': 'password'})
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})
                self.assertEqual(register_request.status_code, 400)
                self.assertEqual(json.loads(register_request.data).get('message'), MessageCode.USER_EXISTS)

    def test_register_and_login_and_refresh_token(self):
        with self.app() as c:
            with self.app_context():
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})
                self.assertEqual(register_request.status_code, 201)
                login_request = c.post('/v1/login', json={'email': 'john.doe@email.com',
                                                          'password': 'password'},
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(login_request.status_code, 200)
                access_token = json.loads(login_request.data).get('access_token')
                refresh_token = json.loads(login_request.data).get('refresh_token')
                self.assertIsNotNone(access_token)
                self.assertIsNotNone(refresh_token)
                refresh_request = c.post('/v1/refresh', headers={'Authorization': 'Bearer ' + refresh_token})
                self.assertEqual(refresh_request.status_code, 200)
                self.assertIn('access_token', json.loads(refresh_request.data).keys())

    def test_register_and_login_and_logout(self):
        with self.app() as c:
            with self.app_context():
                register_request = c.post('/v1/register', json={'email': 'john.doe@email.com',
                                                                'name': 'John',
                                                                'surname': 'Doe',
                                                                'password': 'password'})
                self.assertEqual(register_request.status_code, 201)
                login_request = c.post('/v1/login', json={'email': 'john.doe@email.com',
                                                          'password': 'password'},
                                       headers={'Content-Type': 'application/json'})
                self.assertEqual(login_request.status_code, 200)
                access_token = json.loads(login_request.data).get('access_token')
                refresh_token = json.loads(login_request.data).get('refresh_token')
                self.assertIsNotNone(access_token)
                self.assertIsNotNone(refresh_token)
                logout_request = c.post('/v1/logout', headers={'Authorization': 'Bearer ' + access_token})
                self.assertEqual(logout_request.status_code, 200)
                self.assertEqual(json.loads(logout_request.data).get('message'), MessageCode.USER_LOGGED_OUT)
