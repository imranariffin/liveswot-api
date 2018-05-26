import json

import jwt
from kgb import SpyAgency
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from swot_members.models import SwotMember, Invite

client = Client()


class SignupStatusCodeTestCase(TestCase):
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
                    'email': 'some.valid.email@gmail.com',
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


class SignupResponseDataTestCase(TestCase):
    fixtures = ['users.json']
    valid_data1 = {'user': {
        'email': 'valid.email1@mail.com',
        'username': 'valid.username1',
        'password': 'somevalidpassword',
    }}
    valid_data2 = {'user': {
        'email': 'valid.email2@mail.com',
        'username': 'valid.username2',
        'password': 'somevalidpassword',
    }}
    valid_data3 = {'user': {
        'email': 'valid.email3@mail.com',
        'username': 'valid.username3',
        'password': 'somevalidpassword',
    }}

    def test_successful_signup_respond_with_correct_shape(self):
        response = client.post(
            reverse('authenticationjwt:signup'),
            data=json.dumps(self.valid_data1),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_successful_signup_should_respond_with_correct_information(self):
        response_data = client.post(
            reverse('authenticationjwt:signup'),
            data=json.dumps(self.valid_data2),
            content_type='application/json',
        ).data['data']

        self.assertTrue('user' in response_data)
        self.assertTrue('email' in response_data['user'])
        self.assertTrue('username' in response_data['user'])
        self.assertTrue('token' in response_data['user'])

    def test_successful_signup_should_respond_with_correct_types(self):
        res_data = client.post(
            reverse('authenticationjwt:signup'),
            data=json.dumps(self.valid_data3),
            content_type='application/json'
        ).data['data']

        self.assertTrue(type(res_data['user']) == dict)
        self.assertTrue(type(res_data['user']['email']) == unicode)
        self.assertTrue(type(res_data['user']['username']) == unicode)
        self.assertTrue(type(res_data['user']['token']) == unicode)

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

        user = response.data['data']['user']

        payload = None
        try:
            payload = jwt.decode(user['token'], settings.SECRET_KEY, algorithm='HS256')
        except:
            self.assertEqual(True, False)
        self.assertIsInstance(payload['userId'], int)
        self.assertIsInstance(payload['exp'], int)


class SignupStatusCodeTestCase(TestCase):
    fixtures = ['invites.json', 'members.json', 'swots.json', 'users.json']
    spy_agent = SpyAgency()

    def test_successful_signup_users_with_pending_invites_should_create_memberships(self):
        email = 'pending.invites@liveswot.com'
        username = 'pending.invites'
        password = 'somevalidpassword'
        create_membership = self.spy_agent.spy_on(
            SwotMember.objects.create,
            call_original=False,
        )

        client.post(
            reverse('authenticationjwt:signup'),
            content_type='application/json',
            data=json.dumps({
                'user': {
                    'email': email,
                    'username': username,
                    'password': password,
                }
            })
        )

        n = len(Invite.objects.filter(email=email))
        self.assertEqual(len(create_membership.calls), n)
