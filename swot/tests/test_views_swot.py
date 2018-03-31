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
    post_data = {
        'title': 'Some title',
        'description': 'Some description',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_successful_get_swots_should_respond_with_correct_shape(self):
        response = client.get(
            reverse('swot:get_post', kwargs={}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)

    def test_successful_post_swot_should_respond_with_correct_shape(self):
        response = client.post(
            reverse('swot:get_post', kwargs={}),
            data=json.dumps(self.post_data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)


class GetSwotTestCase(TestCase):
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


class PostSwotTestCase(TestCase):
    fixtures = ['users.json', 'swots.json']
    auth_data = {
        'user': {
            'id': 100,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    post_data = {
        'title': 'Some title',
        'description': 'Some description',
    }
    post_data2 = {
        'title': 'Some other title',
        'description': 'Some other description',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_post_should_create_new_swot(self):
        n = len(client.get(
            reverse('swot:get_post'),
        ).data['data'])

        response = client.post(
            reverse('swot:get_post'),
            data=json.dumps(self.post_data),
            content_type='application/json'
        )

        expected = n + 1
        actual = len(client.get(
            reverse('swot:get_post')
        ).data['data'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(actual, expected)
