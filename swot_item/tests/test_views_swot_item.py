import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleItemTestCase(TestCase):
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

    def test_get_all_items(self):
        response = client.get(reverse('get_post_swot_item'), kwargs={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)

    def test_create_a_valid_strength_item(self):
        response = client.post(
            reverse('get_post_swot_item'),
            data=json.dumps(self.valid_strength),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_a_valid_weakness_item(self):
        response = client.post(
            reverse('get_post_swot_item'),
            data=json.dumps(self.valid_weakness),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_an_invalid_item_wrong_cardtype(self):
        response = client.post(
            reverse('get_post_swot_item'),
            data=json.dumps(self.invalid_item_wrong_cardtype),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_invalid_strength_empty_text(self):
        response = client.post(
            reverse('get_post_swot_item'),
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
            reverse('swot_item_vote:get_post', args=[1]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

    def test_delete_item_should_not_also_delete_votes(self):
        self.assertEqual(
            1,
            len(client.get(
                reverse('swot_item_vote:get_post', args=[1]),
                content_type='application/json'
            ).json())
        )

        client.delete(
            reverse('get_post_swot_item', args=[1]),
            content_type='application/json',
        )

        self.assertEqual(
            status.HTTP_404_NOT_FOUND,
            client.get(
                reverse('get_post_swot_item', args=[1]),
                content_type='application/json'
            ).status_code
        )

        self.assertEqual(
            1,
            len(client.get(
                reverse('swot_item_vote:get_post', args=[1]),
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
        self.assertTrue('Only creator can update Swot Item' in response.data['errors'])

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
