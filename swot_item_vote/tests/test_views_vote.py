import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class SimpleVoteTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_successful_get_should_respond_with_correct_response_shape(self):
        response = client.get(
            reverse('swot_item_vote:get_post', args=[1]),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)

    def test_successful_post_should_respond_with_correct_response_shape(self):
        response = client.post(
            reverse('swot_item_vote:get_post', args=[2]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

    def test_create_new_vote(self):
        item_id = 1

        response = client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'data': {
                'swotItemId': item_id,
                'userId': self.auth_data['user']['userId'],
                'voteType': 'up',
            }
        })

    def test_get_all_votes_should_return_empty_list_when_no_vote(self):
        response = client.get(
            reverse('swot_item_vote:get_post', args=[1]),
            content_type='application/json',
        )

        response_data = response.data

        self.assertEqual(0, len(response_data['data']))

    def test_get_all_votes_should_return_list_with_the_vote_when_one_vote(self):
        client.post(
            reverse('swot_item_vote:get_post', args=[1]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        response = client.get(
            reverse('swot_item_vote:get_post', args=[1]),
        )

        self.assertEqual(1, len(response.json()['data']))


class ErrorVotesTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_vote_non_existing_item_should_repond_404(self):
        response = client.post(
            reverse('swot_item_vote:get_post', args=[99]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MultipleVotesTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        self.vote_up = {
            'voteType': 'up',
        }
        self.vote_down = {'voteType': 'down', }

        testutils.setuptoken(self, self.auth_data, client)

    def test_vote_up_twice_should_neutralize(self):
        item_id = 1

        # first post
        client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        # second post
        response = client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': {}})

    def test_vote_up_then_vote_down_should_delete_up_and_create_down(self):
        item_id = 1

        client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        response = client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'data': {
                'voteType': 'down',
                'swotItemId': item_id,
                'userId': self.auth_data['user']['userId'],
            }
        })

    def test_vote_down_then_vote_up_should_delete_down_and_create_up(self):
        item_id = 1

        client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        response = client.post(
            reverse('swot_item_vote:get_post', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'data': {
                'voteType': 'up',
                'swotItemId': item_id,
                'userId': self.auth_data['user']['userId'],
            }
        })
