from django.test import TestCase
from django.db import IntegrityError

from ..models import SwotMember, Invite


class TestMember(TestCase):
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


class TestInvites(TestCase):
    fixtures = ['invites.json', 'members.json', 'users.json', 'swots.json']

    def test_email_cannot_be_null(self):
        try:
            Invite.objects.create(
                added_by_id=5,
                swot_id=8
            )
            self.fail()
        except IntegrityError:
            pass

    def test_swot_cannot_be_null(self):
        try:
            Invite.objects.create(
                email="imran.ariffin3@liveswot.com",
                added_by_id=5
            )
            self.fail()
        except IntegrityError:
            pass

    def test_added_by_must_be_swot_member(self):
        try:
            Invite.objects.create(
                email="imran.ariffin3@liveswot.com",
                added_by_id=4,
                swot_id=8
            )
            self.fail()
        except IntegrityError:
            pass

    def test_swot_must_be_existing(self): pass

    def test_create_invite_returns_new_invite_object(self):
        try:
            invite = Invite.objects.create(
                email="imran.ariffin3@liveswot.com",
                added_by_id=5,
                swot_id=8
            )
            self.assertIsNotNone(invite)
            self.assertEqual(invite.email, "imran.ariffin3@liveswot.com")
            self.assertEqual(invite.added_by_id, 5)
            self.assertEqual(invite.swot_id, 8)
            self.assertIsNotNone(invite.created)
        except IntegrityError:
            self.fail()
