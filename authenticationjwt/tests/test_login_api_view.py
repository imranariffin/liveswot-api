import json

import jwt
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

client = Client()


class LoginStatusCodeTestCase(TestCase):
    fixtures = ['users.json']

    def test_login_correct_email_password_should_return_200(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'katakunci',
                }
            })
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password_should_return_400(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'wrong',
                },
            })
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_login_non_existing_email_should_return_400(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps({
                'user': {
                    'email': 'non.existing@liveswot.com',
                    'password': 'dontcare',
                },
            })
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

class LoginResponseStructureTestCase(TestCase):
    fixtures = ['users.json']

    def test_success_login_should_return_correct_shape(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'katakunci',
                }
            })
        )

        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_successful_login_should_respond_with_correct_information(self):
        response_data = client.post(
            reverse('authenticationjwt:login'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'katakunci',
                }
            })
        ).data['data']

        self.assertTrue('user' in response_data)
        self.assertTrue('email' in response_data['user'])
        self.assertTrue('username' in response_data['user'])
        self.assertTrue('token' in response_data['user'])

    def test_successful_login_should_respond_with_correct_types(self):
        response_data = client.post(
            reverse('authenticationjwt:login'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'katakunci',
                }
            })
        ).data['data']

        self.assertTrue(type(response_data['user']) == dict)
        self.assertTrue(type(response_data['user']['email']) == unicode)
        self.assertTrue(type(response_data['user']['username']) == unicode)
        self.assertTrue(type(response_data['user']['token']) == unicode)


class LoginTestCase(TestCase):
    fixtures = ['users.json']

    def test_login_wrong_password_should_return_correct_err_message(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'wrongpassword',
                },
            })
        )

        self.assertEqual(
            {"errors": ["There is no such user with the email and password"]},
            response.data,
        )

    def test_login_nonexisting_email_should_return_correct_err_message(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps({
                'user': {
                    'email': 'non.existing@liveswot.com',
                    'password': 'dontcare',
                },
            })
        )

        self.assertEqual(
            {'errors': ['There is no such user with the email and password']},
            response.data
        )

    def test_login_correct_email_password_should_return_user_with_token(self):
        response = client.post(
            reverse('authenticationjwt:login'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'password': 'katakunci',
                }
            })
        )

        user = response.data['data']['user']
        self.assertEqual('imran.ariffin', user['username'])
        self.assertEqual('imran.ariffin@liveswot.com', user['email'])

        payload = jwt.decode(user['token'], settings.SECRET_KEY, algorithm='HS256')
        self.assertEqual(5, payload['id'])
