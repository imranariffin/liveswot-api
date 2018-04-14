import datetime

from django.test import TestCase

from swot_item.models import SwotItem, INIT_SCORE

ITEM_1_TEXT = 'Strength item #1'


class SwotItemTestCase(TestCase):
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

    def test_has_default_score_value(self):
        item = SwotItem.objects.create(
            created_by_id=5,
            swot_id=1,
            text='I have not assigned an initial score value',
        )

        self.assertEqual(item.score, INIT_SCORE)
