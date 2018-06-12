from django.test import TestCase
from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from django.contrib.auth import get_user_model


class UserCreateGet(LoggedInTestCase):
    def setUp(self):
        super(UserCreateGet, self).setUp()
        self.response = self.client.get(r('user-create'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/user/user_create.html')