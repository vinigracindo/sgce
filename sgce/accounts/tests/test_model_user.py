from django.test import TestCase
from django.contrib.auth import get_user_model
from sgce.accounts.models import Profile


class UserModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('user', 'user@mail.com', 'pass')

    def test_profile_create(self):
        """Must create a Profile when user is created."""
        self.assertTrue(Profile.objects.exists())