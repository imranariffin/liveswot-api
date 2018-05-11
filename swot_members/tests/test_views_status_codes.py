import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from utils.testutils import setup_token


client = APIClient()


class TestAddMemberStatusCode(TestCase):
    fixtures = ['members.json', 'swots.json', 'users.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        setup_token(self, self.auth_data, client)

    def test_creator_add_member_success_should_respond_201(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 8,
                'member_id': 6,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_creator_directly_add_member_should_return_403(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 4,
                'member_id': 6,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_member_to_non_existing_swot_should_return_404(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 99,
                'member_id': 6,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_non_existing_user_to_swot_should_return_404(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 4,
                'member_id': 999,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGetMembersStatusCode(TestCase):
    fixtures = ['members.json', 'swots.json', 'users.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        setup_token(self, self.auth_data, client)

    def test_get_members_from_non_existing_swot_should_return_404(self):
        response = client.get(
            reverse('swot_members:get', kwargs={
                'swot_id': 99,
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_members_from_non_member_of_swot_should_return_403(self):
        response = client.get(
            reverse('swot_members:get', kwargs={
                'swot_id': 9,
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
