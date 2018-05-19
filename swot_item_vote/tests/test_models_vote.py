from django.test import TestCase
from django.db import IntegrityError

from swot.models import Swot
from swot_item.models import SwotItem
from swot_item_vote.models import Vote
from authenticationjwt.models import User


class TestVoteModel(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    user, swot, swot_item, vote = None, None, None, None

    def setUp(self):
        try:
            self.user = User.objects.get(email='imran.ariffin@liveswot.com', pk=5)
            self.swot = Swot.objects.get(pk=1, created_by_id=5)
            self.swot_item = SwotItem.objects.get(pk=1, swot_id=1)
            self.vote = Vote.objects.get(pk=1, swot_item_id=1)
        except User.DoesNotExist, udne:
            self.assertTrue(False, udne)
        except Swot.DoesNotExist, sdne:
            self.assertTrue(False, sdne)
        except SwotItem.DoesNotExist, sidne:
            self.assertTrue(False, sidne)
        except Vote.DoesNotExist, vdne:
            self.assertTrue(False, vdne)

        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.swot)
        self.assertIsNotNone(self.swot_item)
        self.assertIsNotNone(self.vote)

    def test_same_user_cannot_have_more_than_one_vote_per_item(self):
        try:
            Vote.objects.create(
                swot_id=self.swot.id,
                swot_item_id=self.swot_item.id,
                created_by_id=self.user.id)
            self.assertTrue(False, "Integrity error expected to be thrown but not thrown")
        except IntegrityError:
            self.assertTrue(True, "Integrity error thrown correctly")

