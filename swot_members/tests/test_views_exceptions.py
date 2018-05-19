import json

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from utils import testutils

client = APIClient()


class TestViewsExceptions(TestCase):
    fixtures = ['members.json', 'swots.json', 'users.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        testutils.setup_token(self, self.auth_data, client)

    def test_non_creator_cannot_add_member(self):
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': 4,
                'member_id': 6,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(
            response.data['errors'],
            ['Not allowed']
        )

    def test_cannot_add_non_existing_member(self):
        swot_id, member_id = 4, 999
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': swot_id,
                'member_id': member_id,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(
            response.data['errors'],
            ['Cannot add non-existing user `{}` to swot `{}`'.format(member_id, swot_id)]
        )

    def test_cannot_add_member_to_non_existing_swot(self):
        swot_id, member_id = 999, 6
        response = client.post(
            reverse('swot_members:post', kwargs={
                'swot_id': swot_id,
                'member_id': member_id,
            }),
            data=json.dumps({}),
            content_type='application/json',
        )

        self.assertEqual(
            response.data['errors'],
            ['Cannot add user `{}` to non-existing swot `{}`'.format(member_id, swot_id)]
        )
