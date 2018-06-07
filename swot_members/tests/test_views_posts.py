import json

from kgb import SpyAgency
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from utils.testutils import setup_token
from ..models import Invite
from ..utils import send_invite_email

client = APIClient()


class TestViewsPostResponseShape(TestCase):
    fixtures = ['members.json', 'swots.json', 'users.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        setup_token(self, self.auth_data, client)

    def test_success_should_return_correct_shape(self):
        response_data = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'email': 'testuser4@liveswot.com',
            }),
            data=json.dumps({}),
            content_type='application/json'
        ).data

        self.assertEqual(type(response_data), dict)
        self.assertEqual(type(response_data['data']), dict)

    def test_success_should_return_correct_information(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'email': 'testuser4@liveswot.com',
            }),
            content_type='application/json',
            data=json.dumps({})
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.data['data']

        self.assertTrue('swotId' in response_data)
        self.assertTrue('memberId' in response_data)
        self.assertTrue('membershipId' in response_data)
        self.assertTrue('created' in response_data)
        self.assertTrue('addedById' in response_data)

    def test_success_existing_user_respond_with_correct_data_types(self):
        response_data = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'email': 'testuser4@liveswot.com',
            }),
            content_type='application/json',
            data=json.dumps({})
        ).data['data']

        self.assertTrue(type(response_data['memberId']) == int)
        self.assertTrue(type(response_data['membershipId']) == int)
        self.assertTrue(type(response_data['swotId']) == int)
        self.assertTrue(type(response_data['addedById']) == int)

    def test_success_existing_user_respond_with_correct_data_types(self):
        response_data = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'email': 'nonexisting@liveswot.com',
            }),
            content_type='application/json',
            data=json.dumps({})
        ).data['data']

        self.assertTrue(len(response_data) == 0)


class TestViewsPost(TestCase):
    fixtures = ['members.json', 'swots.json', 'users.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    spy_agent = SpyAgency()

    def setUp(self):
        setup_token(self, self.auth_data, client)

    def test_add_member_non_existing_user_should_create_invite(self):
        n = len(Invite.objects.all())
        client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'email': 'nonexisting@gmail.com',
            }),
            content_type='application/json',
            data=json.dumps({})
        )
        actual = len(Invite.objects.all())

        self.assertEqual(actual, n + 1)

    def test_add_member_non_existing_should_send_email(self):
        swot_id, email = 8, 'ariffin.imran@gmail.com'
        invitor = 'imran.ariffin@liveswot.com'
        mock_send_email = self.spy_agent.spy_on(send_invite_email, call_original=False)

        client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': swot_id,
                'email': email,
            }),
            content_type='application/json',
            data=json.dumps({})
        )

        self.assertTrue(mock_send_email.called_with(invitor, email))

