import json
from swot.serializers import SwotItemSerializer
from swot.models import SwotItem
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()

class SimpleItemTestCase(TestCase):
    fixtures = ['items.json']

    def setUp(self):
        self.valid_strength = {
        	'cardType': 'strength',
        	'text': 'Strength item #1',
        }
        self.valid_strength2 = {
        	'cardType': 'strength',
        	'text': 'Strength item #2',
        }
        self.valid_weakness = {
        	'cardType': 'weakness',
        	'text': 'Weakness item #1',
        }
        self.invalid_item_wrong_cardtype = {
        	'cardType': 'something',
        	'text': 'Invalid item #1',
        }
        self.invalid_item2_empty_text = {
        	'cardType': 'strength',
        	'text': '',
        }

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

	def test_get_all_items(self):
		response = client.get(reverse('get_post_delete_swot_item'), kwargs={})
		items = SwotItem.objects.all()
		serializer = SwotItemSerializer(items, many=True)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)
		self.assertEqual(response.data, serializer.data)

	def test_create_a_valid_strength_item(self):
		response = client.post(
			reverse('get_post_delete_swot_item'),
			data=json.dumps(self.valid_strength),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_a_valid_weakness_item(self):
		response = client.post(
			reverse('get_post_delete_swot_item'),
			data=json.dumps(self.valid_weakness),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_an_invalid_item_wrong_cardtype(self):
		response = client.post(
			reverse('get_post_delete_swot_item'),
			data=json.dumps(self.invalid_item_wrong_cardtype),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_an_invalid_strength_empty_text(self):
		response = client.post(
			reverse('get_post_delete_swot_item'),
			data=json.dumps(self.invalid_item2_empty_text),
			content_type='application/json',
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ItemDeletionTestCase(TestCase):
	fixtures = ['items.json']
	def setUp(self):
		self.vote_up = {
			'item': 1,
			'voteType': 'up',
		}
		client.post(
			reverse('get_post_vote', args=[1]),
			data=json.dumps(self.vote_up),
			content_type='application/json',
		)

	# def test_delete_item_should_also_delete_votes(self):
	# 	self.assertEqual(
	# 		1,
	# 		len(client.get(
	# 			reverse('get_post_vote', args=[1]),
	# 			content_type='application/json'
	# 		).json())
	# 	)
  #
	# 	client.delete(
	# 		reverse('get_post_delete_swot_item', args=[1]),
	# 		content_type='application/json',
	# 	)
  #
	# 	self.assertEqual(
	# 		status.HTTP_404_NOT_FOUND,
	# 		client.get(
	# 			reverse('get_post_delete_swot_item', args=[1]),
	# 			content_type='application/json'
	# 		).status_code
	# 	)
	# 	self.assertEqual(
	# 		0,
	# 		len(client.get(
	# 			reverse('get_post_vote', args=[1]),
	# 			content_type='application/json'
	# 		).json())
	# 	)
