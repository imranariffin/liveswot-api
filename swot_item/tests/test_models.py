import datetime

from django.test import TestCase

from swot_item.models import SwotItem
from swot_item_vote.models import Vote

ITEM_1_TEXT = 'Strength item #1'


class ItemTestCase(TestCase):
    fixtures = ['swotItems.json']

    def setUp(self):
        pass

    def test_item_has_created_field(self):
        '''
        date created is automatically created
        '''
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        self.assertIn('created', dir(item1))
        self.assertIsInstance(item1.created, datetime.datetime)

    def test_item_has_votes(self):
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        vote = Vote.objects.create(item=item1)
        self.assertIn(vote, item1.vote_set.all())
        self.assertEqual(vote.id, item1.vote_set.first().id)

    def test_item_has_multiple_votes(self):
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        votes = [item1.vote_set.create() for x in range(5)]
        self.assertEqual(len(item1.vote_set.all()), len(votes))
        self.assertEqual(set(item1.vote_set.all()), set(votes))

    def test_vote_has_one_item(self):
        item1 = SwotItem.objects.filter(text=ITEM_1_TEXT).first()
        vote = Vote.objects.create(item=item1)
        self.assertEqual(vote.item.id, item1.id)
