import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleSwotTestCase(TestCase):
    fixtures = ['users.json', 'swots.json']
    auth_data = {
        'user': {
            'id': 100,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_get_all_swots(self):
        response = client.get(
            reverse('swot:get_post', kwargs={})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)
        self.assertTrue(len(response.data['data']) > 0)

        response_data = response.data['data']
        user = self.auth_data['user']

        self.assertTrue(
            all([user['id'] != swot['owner'] for swot in response_data])
        )

    def test_get_swots_without_token_should_error(self):
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.get(
            reverse('swot:get_post', kwargs={})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
