import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from utils.testutils import setup_token

client = APIClient()


class TestViewsGet(TestCase):
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

    def test_success_respond_with_correct_shape(self):
        response_data = client.get(
            reverse('swot_members:get', kwargs={
                'swot_id': 8,
            }),
            content_type='application/json'
        ).data

        self.assertEqual(type(response_data), dict)
        self.assertEqual(type(response_data['data']), list)

        list_data = response_data['data']

        self.assertTrue(all([type(d) == dict for d in list_data]))

    def test_success_respond_with_correct_information(self):
        response_data = client.get(
            reverse('swot_members:get', kwargs={
                'swot_id': 8,
            }),
            content_type='application/json'
        ).data['data']

        self.assertTrue(all(['memberId' in d for d in response_data]))
        self.assertTrue(all(['membershipId' in d for d in response_data]))
        self.assertTrue(all(['swotId' in d for d in response_data]))
        self.assertTrue(all(['addedById' in d for d in response_data]))
        self.assertTrue(all(['created' in d for d in response_data]))

    def test_success_respond_with_correct_data_types(self):
        response_data = client.get(
            reverse('swot_members:get', kwargs={
                'swot_id': 8,
            }),
            content_type='application/json'
        ).data['data']

        self.assertTrue(all([type(d['memberId']) == int for d in response_data]))
        self.assertTrue(all([type(d['membershipId']) == int for d in response_data]))
        self.assertTrue(all([type(d['swotId']) == int for d in response_data]))
        self.assertTrue(all([type(d['addedById']) == int for d in response_data]))
