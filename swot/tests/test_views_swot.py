import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleGetSwotTestCase(TestCase):
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

    def test_successful_get_swots_should_respond_with_correct_shape(self):
        response = client.get(
            reverse('swot:get_post', kwargs={}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)

        response_data = response.data['data']
        self.assertEqual(type(response_data), list)

    def test_successful_get_swots_should_respond_with_correct_information(self):
        response_data = client.get(
            reverse('swot:get_post', kwargs={}),
        ).data['data']

        self.assertTrue(all(['swotId' in swot for swot in response_data]))
        self.assertTrue(all(['creatorId' in swot for swot in response_data]))
        self.assertTrue(all(['title' in swot for swot in response_data]))
        self.assertTrue(all(['description' in swot for swot in response_data]))

    def test_successful_get_swots_should_respond_with_correct_types(self):
        res_data = client.get(
            reverse('swot:get_post', kwargs={}),
        ).data['data']

        self.assertTrue(all([type(swot['swotId']) == int for swot in res_data]))
        self.assertTrue(all([type(swot['creatorId']) == int for swot in res_data]))
        self.assertTrue(all([type(swot['title']) == unicode for swot in res_data]))
        self.assertTrue(all([type(swot['description']) == unicode for swot in res_data]))


class SimplePostSwotTestCase(TestCase):
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

    def test_successful_post_swot_should_respond_with_correct_shape(self):
        response = client.post(
            reverse('swot:get_post', kwargs={}),
            data=json.dumps(self.post_data),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_successful_post_swots_should_respond_with_correct_information(self):
        response_data = client.post(
            reverse('swot:get_post', kwargs={}),
            data=json.dumps(self.post_data),
            content_type='application/json'
        ).data['data']

        self.assertTrue('swotId' in response_data)
        self.assertTrue('creatorId' in response_data)
        self.assertTrue('title' in response_data)
        self.assertTrue('description' in response_data)

    def test_successful_post_swots_should_respond_with_correct_types(self):
        res_data = client.post(
            reverse('swot:get_post', kwargs={}),
            data=json.dumps(self.post_data),
            content_type='application/json'
        ).data['data']

        self.assertTrue(type(res_data['swotId']) == int)
        self.assertTrue(type(res_data['creatorId']) == int)
        self.assertTrue(type(res_data['title']) == unicode)
        self.assertTrue(type(res_data['description']) == unicode)


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
        testutils.setuptoken(self, self.auth_data, client)

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


class SimpleDeleteSwotTestCase(TestCase):
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

    def test_successful_put_swot_should_respond_with_correct_shape(self):
        response = client.delete(
            reverse('swot:put_delete', args=[1]),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
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
            all([user['id'] != swot['creatorId'] for swot in response_data])
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


class DeleteSwotTestCase(TestCase):
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

    def test_successful_delete_should_remove_swot_from_db(self):

        n = len(client.get(reverse('swot:get_post')).data['data'])
        self.assertNotEqual(n, 0)

        expected = n - 1

        response = client.delete(
            reverse('swot:put_delete', args=[1]),
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
        self.assertEqual(response.data['errors'][0], 'Only creator can delete swot')

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
