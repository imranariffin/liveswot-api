import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from utils.testutils import setup_token

client = APIClient()


class TestViewsPost(TestCase):
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
                'member_id': 6,
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
                'member_id': 6,
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

    def test_success_respond_with_correct_data_types(self):
        response_data = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'member_id': 6,
            }),
            content_type='application/json',
            data=json.dumps({})
        ).data['data']

        self.assertTrue(type(response_data['memberId']) == int)
        self.assertTrue(type(response_data['membershipId']) == int)
        self.assertTrue(type(response_data['swotId']) == int)
        self.assertTrue(type(response_data['addedById']) == int)