import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class ShapeSwotItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    post_data = {
        'cardType': 'strength',
        'text': 'Strength item #1',
    }
    put_data = {
        'swotItemId': 1,
        'cardType': 'strength',
        'text': 'New text in PUT',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_success_get_all_items_returns_correct_shape(self):
        response = client.get(reverse('get_post_swot_item', kwargs={'swot_id': 1}))

        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)
        items = response.data['data']
        self.assertTrue(all([type(item) == dict for item in items]))

    def test_success_get_all_items_returns_correct_information(self):
        response = client.get(reverse('get_post_swot_item', kwargs={'swot_id': 1}))
        items = response.data['data']

        self.assertTrue(all(['swotItemId' in item for item in items]))
        self.assertTrue(all(['creatorId' in item for item in items]))
        self.assertTrue(all(['swotId' in item for item in items]))
        self.assertTrue(all(['text' in item for item in items]))
        self.assertTrue(all(['cardType' in item for item in items]))

    def test_success_get_all_items_returns_correct_types(self):
        response = client.get(reverse('get_post_swot_item', kwargs={'swot_id': 1}))
        items = response.data['data']

        self.assertTrue(all([type(item['swotItemId']) == int for item in items]))
        self.assertTrue(all([type(item['creatorId']) == int for item in items]))
        self.assertTrue(all([type(item['swotId']) == int for item in items]))
        self.assertTrue(all([type(item['text']) == unicode for item in items]))
        self.assertTrue(all([type(item['cardType']) == unicode for item in items]))

    def test_success_post_swot_items_returns_correct_shape(self):
        response = client.post(
            reverse('get_post_swot_item', kwargs={'swot_id': 1}),
            data=json.dumps(self.post_data),
            content_type='application/json',
        )

        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_success_post_swot_items_returns_correct_information(self):
        response = client.post(
            reverse('get_post_swot_item', kwargs={'swot_id': 1}),
            data=json.dumps(self.post_data),
            content_type='application/json',
        )

        response_data = response.data['data']

        self.assertTrue('swotItemId' in response_data)
        self.assertTrue('swotId' in response_data)
        self.assertTrue('creatorId' in response_data)
        self.assertTrue('text' in response_data)
        self.assertTrue('cardType' in response_data)

    def test_success_post_swot_items_returns_correct_types(self):
        response = client.post(
            reverse('get_post_swot_item', kwargs={'swot_id': 1}),
            data=json.dumps(self.post_data),
            content_type='application/json',
        )

        swot_item = response.data['data']

        self.assertTrue(type(swot_item['swotItemId']) == int)
        self.assertTrue(type(swot_item['swotId']) == int)
        self.assertTrue(type(swot_item['creatorId']) == int)
        self.assertTrue(type(swot_item['text']) == unicode)
        self.assertTrue(type(swot_item['cardType']) == unicode)

    def test_success_delete_swot_item_returns_correct_shape(self):
        response = client.delete(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
        )

        self.assertTrue(type(response.data) == dict)
        self.assertTrue(type(response.data['data']) == dict)

    def test_success_delete_swot_item_returns_correct_information(self):
        response = client.delete(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
        )

        self.assertTrue(len(response.data['data']) == 0)

    def test_success_put_swot_item_returns_correct_shape(self):
        response = client.put(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
            data=json.dumps(self.put_data),
            content_type='application/json',
        )

        self.assertTrue(type(response.data) == dict)
        self.assertTrue(type(response.data['data']) == dict)

    def test_success_put_swot_item_returns_correct_information(self):
        response = client.put(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
            data=json.dumps(self.put_data),
            content_type='application/json',
        )

        response_data = response.data['data']

        self.assertTrue('swotItemId' in response_data)
        self.assertTrue('swotId' in response_data)
        self.assertTrue('creatorId' in response_data)
        self.assertTrue('text' in response_data)
        self.assertTrue('cardType' in response_data)

    def test_success_put_swot_items_returns_correct_types(self):
        response = client.put(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
            data=json.dumps(self.put_data),
            content_type='application/json',
        )

        swot_item = response.data['data']

        self.assertTrue(type(swot_item['swotItemId']) == int)
        self.assertTrue(type(swot_item['swotId']) == int)
        self.assertTrue(type(swot_item['creatorId']) == int)
        self.assertTrue(type(swot_item['text']) == unicode)
        self.assertTrue(type(swot_item['cardType']) == unicode)


class GetSwotItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_success_get_all_items_returns_200(self):
        response = client.get(reverse('get_post_swot_item', kwargs={'swot_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_items_non_existing_swot_returns_404(self):
        pass

    def test_get_all_items_no_token_returns_403(self):
        pass


class PostSwotItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    valid_strength = {
        'cardType': 'strength',
        'text': 'Strength item #1',
    }
    valid_strength2 = {
        'cardType': 'strength',
        'text': 'Strength item #2',
    }
    valid_weakness = {
        'cardType': 'weakness',
        'text': 'Weakness item #1',
    }
    invalid_item_wrong_cardtype = {
        'cardType': 'something',
        'text': 'Invalid item #1',
    }
    invalid_item2_empty_text = {
        'cardType': 'strength',
        'text': '',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_create_a_valid_strength_item(self):
        response = client.post(
            reverse('get_post_swot_item', kwargs={'swot_id': 1}),
            data=json.dumps(self.valid_strength),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_valid_weakness_item(self):
        response = client.post(
            reverse('get_post_swot_item', args=[1]),
            data=json.dumps(self.valid_weakness),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_an_invalid_item_wrong_cardtype(self):
        response = client.post(
            reverse('get_post_swot_item', args=[1]),
            data=json.dumps(self.invalid_item_wrong_cardtype),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_invalid_strength_empty_text(self):
        response = client.post(
            reverse('get_post_swot_item', args=[1]),
            data=json.dumps(self.invalid_item2_empty_text),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSwotItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'swot_item_id': 1,
        'voteType': 'up',
    }

    def setUp(self):

        testutils.setuptoken(self, self.auth_data, client)
        client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': 1}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

    def test_delete_item_should_not_also_delete_votes(self):
        self.assertEqual(
            1,
            len(client.get(
                reverse('swot_item_vote:get', kwargs={'swot_id': 1}),
                content_type='application/json'
            ).json())
        )

        n = len(client.get(
            reverse('get_post_swot_item', kwargs={'swot_id': 1})
        ).data['data'])

        client.delete(
            reverse('put_delete_swot_item', kwargs={'swot_item_id': 1}),
            content_type='application/json',
        )

        self.assertEqual(
            n - 1,
            len(client.get(
                reverse('get_post_swot_item', kwargs={'swot_id': 1})
            ).data['data'])
        )

        self.assertEqual(
            1,
            len(client.get(
                reverse('swot_item_vote:get', kwargs={'swot_id': 1}),
                content_type='application/json'
            ).json())
        )


class PutSwotItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    put_data = {
        'text': 'New text',
        'cardType': 'strength'
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_put_success_should_return_200(self):
        response = client.put(
            reverse('put_delete_swot_item', args=[1]),
            data=json.dumps(self.put_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_success_should_return_updated_swot_item(self):
        response = client.put(
            reverse('put_delete_swot_item', args=[1]),
            data=json.dumps(self.put_data),
            content_type='application/json'
        )

        self.assertEqual(
            response.data['data']['text'],
            self.put_data['text']
        )

    def test_put_invalid_empty_text_in_body_should_return_400(self):
        response = client.put(
            reverse('put_delete_swot_item', args=[1]),
            data=json.dumps({
                'text': ''
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(len(response.data['errors']) >= 1)
        self.assertTrue('`text` field cannot be empty' in response.data['errors'][0])

    def test_put_non_creator_should_return_403(self):
        response = client.put(
            reverse('put_delete_swot_item', args=[3]),
            data=json.dumps({
                'text': 'New text',
                'cardType': 'strength'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(len(response.data['errors']) >= 1)
        self.assertTrue('Only creator can update/delete Swot Item' in response.data['errors'])

    def test_put_non_existing_swot_item_should_return_404(self):
        response = client.put(
            reverse('put_delete_swot_item', args=[99]),
            data=json.dumps({
                'text': 'New text',
                'cardType': 'strength'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected = 'SwotItem matching query does not exist.'
        self.assertTrue(expected in response.data['errors'])
