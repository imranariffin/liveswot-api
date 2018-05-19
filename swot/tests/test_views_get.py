from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleGetSwotTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'members.json']
    auth_data = {
        'user': {
            'id': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        testutils.setup_token(self, self.auth_data, client)

    def test_successful_get_swots_should_respond_with_correct_shape(self):
        response = client.get(
            reverse('swot:get_post', kwargs={}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)

        response_data = response.data['data']
        self.assertTrue(len(response_data) > 0)
        self.assertEqual(type(response_data), list)

    def test_successful_get_swots_should_respond_with_correct_information(self):
        response_data = client.get(
            reverse('swot:get_post', kwargs={}),
        ).data['data']

        self.assertTrue(len(response_data) > 0)
        self.assertTrue(all(['swotId' in swot for swot in response_data]))
        self.assertTrue(all(['creatorId' in swot for swot in response_data]))
        self.assertTrue(all(['title' in swot for swot in response_data]))
        self.assertTrue(all(['description' in swot for swot in response_data]))
        self.assertTrue(all(['createdAt' in swot for swot in response_data]))

    def test_successful_get_swots_should_respond_with_correct_types(self):
        res_data = client.get(
            reverse('swot:get_post', kwargs={}),
        ).data['data']

        self.assertTrue(len(res_data) > 0)
        self.assertTrue(all([type(swot['swotId']) == int for swot in res_data]))
        self.assertTrue(all([type(swot['creatorId']) == int for swot in res_data]))
        self.assertTrue(all([type(swot['title']) == unicode for swot in res_data]))
        self.assertTrue(all([type(swot['description']) == unicode for swot in res_data]))
        self.assertTrue(all([type(swot['createdAt']) == unicode for swot in res_data]))


class GetSwotTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'members.json']
    auth_data = {
        'user': {
            'id': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        testutils.setup_token(self, self.auth_data, client)

    def test_get_all_swots(self):
        response = client.get(
            reverse('swot:get_post', kwargs={})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)
        self.assertTrue(len(response.data['data']) > 0)
        self.assertEqual(
            set([2, 3, 5, 8]),
            set([sw['swotId'] for sw in response.data['data']]),
        )

    def test_get_swots_without_token_should_error(self):
        client.credentials(HTTP_AUTHORIZATION='')
        response = client.get(
            reverse('swot:get_post', kwargs={})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
