from django.test import TestCase
from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from django.contrib.auth import get_user_model


class UserListGet(LoggedInTestCase):
    def setUp(self):
        super(UserListGet, self).setUp()
        get_user_model().objects.create_user(
            username='user1',
            email='user1@domain.com',
            password='user1password',
            first_name='User',
            last_name='One'
        )
        get_user_model().objects.create_user(
            username='user2',
            email='user2@domain.com',
            password='user2password',
            first_name='User',
            last_name='Two'
        )
        self.response = self.client.get(r('core:user-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/user/user_list.html')

    def test_html(self):
        contents = [
            (1, 'User One'),
            (1, 'user1@domain.com'),
            (1, 'User Two'),
            (1, 'user2@domain.com'),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:user-create'))),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['users']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)