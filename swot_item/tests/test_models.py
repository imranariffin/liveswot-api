import datetime

from django.test import TestCase

from swot_item.models import SwotItem
from swot_item_vote.models import Vote

ITEM_1_TEXT = 'Strength item #1'


class ItemTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json']

    def setUp(self):
        pass

    def test_item_has_created_field(self):
        """
        date created is automatically created
        """
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        self.assertIn('created', dir(item1))
        self.assertIsInstance(item1.created, datetime.datetime)

    def test_vote_has_one_item(self):
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        vote = Vote.objects.create(item=item1)
        self.assertEqual(vote.item.id, item1.id)
