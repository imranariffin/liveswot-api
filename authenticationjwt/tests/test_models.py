from authenticationjwt.models import User

from django.test import TestCase


class TestUserModelPasswordHash(TestCase):

    def test_password_saved_should_be_hashed(self):
        password = 'katakunci'
        user = User.objects.create_user(
            email='someuser@liveswot.com',
            username='someuser',
            password=password,
        )
        user.save()

        self.assertNotEqual(password, user.password)