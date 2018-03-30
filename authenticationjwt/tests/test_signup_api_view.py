import json

import jwt
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

client = Client()


class SignUpAPIViewStatusCodeTestCase(TestCase):
    fixtures = ['users.json']

    def test_signup_empty_password_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'valid.email@liveswot.com',
                    'username': 'valid.username',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_existing_email_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'imran.ariffin@liveswot.com',
                    'username': 'imran.ariffin',
                    'password': 'somevalidpassword',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_empty_email_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'username': 'valid.username',
                    'password': 'somevalidpassword',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_invalid_email_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'invalid.email',
                    'username': 'valid.username',
                    'password': 'somevalidpassword',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_invalid_password_too_short_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'invalid.email',
                    'username': 'valid.username',
                    'password': 'short',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_existing_username_returns_400(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'valid.email@mail.com',
                    'username': 'imran.ariffin',
                    'password': 'somevalidpassword',
                }}))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_signup_valid_returns_201(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'valid.email@mail.com',
                    'username': 'valid.username',
                    'password': 'somevalidpassword',
                }}))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class SignUpAPIViewStatusCodeTestCase(TestCase):
    fixtures = ['users.json']

    def test_sign_valid_returns_email_username_and_token(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'valid.email2@mail.com',
                    'username': 'valid.username2',
                    'password': 'somevalidpassword',
                }}))

        user = response.data

        self.assertIsNotNone(user)
        self.assertIsNotNone(user['token'])
        self.assertEqual(user['email'], 'valid.email2@mail.com')
        self.assertEqual(user['username'], 'valid.username2')

    def test_sign_valid_returns_token_with_id_and_expiration(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': 'valid.email3@mail.com',
                    'username': 'valid.username3',
                    'password': 'somevalidpassword',
                }}))

        user = response.data

        payload = None
        try:
            payload = jwt.decode(user['token'], settings.SECRET_KEY, algorithm='HS256')
        except:
            self.assertEqual(True, False)
        self.assertIsInstance(payload['id'], int)
        self.assertIsInstance(payload['exp'], int)
