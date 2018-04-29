from django.test import TestCase
from django.db import IntegrityError

from swot.models import Swot

from ..models import SwotMember

from authenticationjwt.models import User


class TestModel(TestCase):
    fixtures = ['members.json', 'users.json', 'swots.json']

    def setUp(self):
        pass

    def test_member_cannot_be_null(self):
        try:
            SwotMember.objects.create(
                added_by_id=1,
            )
            self.assertTrue(False)
        except IntegrityError:
            pass

    def test_add_by_cannot_be_null(self):
        try:
            SwotMember.objects.create(
                member_id=1,
            )
            self.assertTrue(False)
            self.assertTrue(False)
        except IntegrityError:
            pass

    def test_member_and_swot_must_be_unique(self):
        try:
            swot_member = SwotMember.objects.create(
                added_by_id=5,
                member_id=2,
                swot_id=8,
            )
            self.fail()
        except IntegrityError:
            pass

    def test_added_by_must_be_member_of_swot(self):
        try:
            SwotMember.objects.create(
                added_by_id=4,
                member_id=4,
                swot_id=8,
            )
            self.fail()
        except IntegrityError:
            pass
