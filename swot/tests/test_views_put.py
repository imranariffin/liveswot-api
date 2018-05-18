import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimplePutSwotTestCase(TestCase):
    fixtures = ['users.json', 'swots.json']
    auth_data = {
        'user': {
            'id': 100,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    put_data = {
        'title': 'Some title',
        'description': 'Some description',
    }

    def setUp(self):
        testutils.setup_token(self, self.auth_data, client)

    def test_successful_put_swot_should_respond_with_correct_shape(self):
        response = client.put(
            reverse('swot:put_delete', args=[1]),
            data=json.dumps(self.put_data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_successful_put_swots_should_respond_with_correct_information(self):
        response_data = client.put(
            reverse('swot:put_delete', args=[1]),
            data=json.dumps(self.put_data),
            content_type='application/json'
        ).data['data']

        self.assertTrue('swotId' in response_data)
        self.assertTrue('creatorId' in response_data)
        self.assertTrue('title' in response_data)
        self.assertTrue('description' in response_data)

    def test_successful_put_swots_should_respond_with_correct_types(self):
        res_data = client.put(
            reverse('swot:put_delete', args=[1]),
            data=json.dumps(self.put_data),
            content_type='application/json'
        ).data['data']

        self.assertTrue(type(res_data['swotId']) == int)
        self.assertTrue(type(res_data['creatorId']) == int)
        self.assertTrue(type(res_data['title']) == unicode)
        self.assertTrue(type(res_data['description']) == unicode)