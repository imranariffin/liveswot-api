import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()


class SimpleVoteTestCase(TestCase):
    fixtures = ['items.json', 'users.json', ]

    def setUp(self):
        self.vote_up = {'voteType': 'up', }

        auth_data = {'user':
                         {'email': 'imran.ariffin@liveswot.com', 'password': 'katakunci'}
                     }
        gettoken_response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps(auth_data))

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + gettoken_response.data['token']
        )

        self.token = gettoken_response.data['token']

    def test_vote_non_existing_item_should_repond_404(self):
        response = client.post(
            reverse('get_post_vote', args=[99]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_new_vote(self):
        item_id = 1

        response = client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'vote': 1,
            'last_vote': {
                'id': 1,
                'voteType': 'up',
                'item': item_id,
            },
        })

    def test_get_all_votes_should_return_empty_list_when_no_vote(self):
        response = client.get(
            reverse('get_post_vote', args=[1]),
            content_type='application/json',
        )

        self.assertEqual(0, len(response.json()))

    def test_get_all_votes_should_return_list_with_the_vote_when_one_vote(self):
        client.post(
            reverse('get_post_vote', args=[1]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        response = client.get(
            reverse('get_post_vote', args=[1]),
            content_type='application/json',
        )

        self.assertEqual(1, len(response.json()))


class MultipleVotesTestCase(TestCase):
    fixtures = ['items.json', 'users.json', ]

    def setUp(self):
        self.vote_up = {'voteType': 'up', }
        self.vote_down = {'voteType': 'down', }

        auth_data = {
            'user': {
                'email': 'imran.ariffin@liveswot.com', 'password': 'katakunci'
            }
        }

        gettoken_response = client.post(
            reverse('authenticationjwt:login'),
            content_type="application/json",
            data=json.dumps(auth_data))

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + gettoken_response.data['token']
        )

        self.token = gettoken_response.data['token']

    def test_vote_up_twice_should_neutralize(self):
        item_id = 1

        # first post
        client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        # second post
        response = client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'vote': 0,
            'last_vote': None,
        })

    def test_vote_up_then_vote_down_should_delete_up_and_create_down(self):
        item_id = 1

        client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        response = client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'vote': -1,
            'last_vote': {
                'id': 2,
                'item': item_id,
                'voteType': 'down'
            }
        })

    def test_vote_down_then_vote_up_should_delete_down_and_create_up(self):
        item_id = 1

        client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        response = client.post(
            reverse('get_post_vote', args=[item_id]),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'vote': 1,
            'last_vote': {
                'id': 2,
                'item': item_id,
                'voteType': 'up'
            }
        })
