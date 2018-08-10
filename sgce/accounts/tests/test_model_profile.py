from django.test import TestCase
from django.contrib.auth import get_user_model
from model_mommy import mommy

from sgce.accounts.models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        # When a user is created a profile is created too.
        self.profile = user.profile

    def test_create(self):
        self.assertTrue(Profile.objects.exists())

    def test_phone_can_be_blank(self):
        field = Profile._meta.get_field('phone')
        self.assertTrue(field.blank)

    def test_str(self):
        self.assertEqual('Perfil de {}'.format(self.profile.user.get_full_name()), str(self.profile))