from django.test import TestCase
from django.db import IntegrityError

from swot.models import Swot
from swot_item.models import SwotItem
from swot_item_vote.models import Vote
from authenticationjwt.models import User


class VoteModelTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    user, swot, swot_item, vote = None, None, None, None

    def setUp(self):
        try:
            self.user = User.objects.get(email='imran.ariffin@liveswot.com', pk=5)
        except User.DoesNotExist, udne:
            self.assertTrue(False, udne)
        print self.user

        try:
            self.swot = Swot.objects.get(pk=1, created_by_id=5)
        except Swot.DoesNotExist, sdne:
            self.assertTrue(False, sdne)
        print self.swot

        try:
            self.swot_item = SwotItem.objects.get(pk=1, swot_id=1)
        except SwotItem.DoesNotExist, sidne:
            self.assertTrue(False, sidne)
        print self.swot_item

        try:
            self.vote = Vote.objects.get(pk=1, swot_item_id=1)
        except Vote.DoesNotExist, vdne:
            print 'Huh?'
            self.assertTrue(False, vdne)
        print self.vote

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
            self.assertTrue(True, "Integrity error thrown corectly")