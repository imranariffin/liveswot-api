from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleDeleteSwotTestCase(TestCase):
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

    def test_successful_put_swot_should_respond_with_correct_shape(self):
        response = client.delete(
            reverse('swot:put_delete', args=[3]),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)


class DeleteSwotTestCase(TestCase):
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

    def test_successful_delete_should_remove_swot_from_db(self):

        swots = client.get(reverse('swot:get_post')).data['data']
        n = len(swots)
        self.assertNotEqual(n, 0)

        expected = n - 1

        response = client.delete(
            reverse('swot:put_delete', args=[swots[0]['swotId']]),
            content_type='application/json'
        )

        actual = len(client.get(reverse('swot:get_post')).data['data'])

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(actual, expected)

    def test_non_creator_can_not_delete(self):
        response = client.delete(
            reverse('swot:put_delete', args=[4]),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0], 'Only creator can delete/modify swot')

    def test_respond_403_for_non_authenticated_request(self):
        client.credentials(HTTP_AUTHORIZATION='')

        response = client.delete(
            reverse('swot:put_delete', args=[4]),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_respond_404_for_non_existing_swot(self):
        response = client.delete(
            reverse('swot:put_delete', args=[999]),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
