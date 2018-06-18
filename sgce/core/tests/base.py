from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from django.conf import settings


class LoggedInTestCase(TestCase):

    def setUp(self):
        get_user_model().objects.create_superuser(username='username', email=None, password='password')
        self.response = self.client.login(username='username', password='password')