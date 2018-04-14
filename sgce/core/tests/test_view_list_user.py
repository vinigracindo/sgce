from django.test import TestCase
from django.shortcuts import resolve_url as r

from sgce.core.models import User


class UserListGet(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('user1', 'user1@domain.com', 'user1password')
        u1.first_name = 'User'
        u1.last_name = 'One'
        u1.save()
        u2 = User.objects.create_user('user2', 'user2@domain.com', 'user2password')
        u2.first_name = 'User'
        u2.last_name = 'Two'
        u2.save()

        self.response = self.client.get(r('user_list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/user_list.html')

    def test_html(self):
        contents = [
            (1, 'Nome'),
            (1, 'Email'),
            (1, 'Ação'),
            (1, 'User One'),
            (1, 'User Two'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)