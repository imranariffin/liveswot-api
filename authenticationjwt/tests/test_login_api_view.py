import json

import jwt
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

client = Client()


class LoginAPIViewTestCase(TestCase):
    fixtures = ['users.json']

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

    def test_login_nonexisting_email_should_return_400(self):
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

        user = response.data
        self.assertEqual('imran.ariffin', user['username'])
        self.assertEqual('imran.ariffin@liveswot.com', user['email'])

        payload = jwt.decode(user['token'], settings.SECRET_KEY, algorithm='HS256')
        self.assertEqual(5, payload['id'])
