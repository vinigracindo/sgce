from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.core.tests.base import LoggedInTestCase
from django.contrib.auth import get_user_model


class UserListWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(UserListWithoutPermission, self).setUp()
        self.response = self.client.get(r('accounts:user-list'))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Permission: auth.view_user
class UserListWithPermission(LoggedInTestCase):
    def setUp(self):
        super(UserListWithPermission, self).setUp()
        # permission required: profile.can_enable_or_disable_user
        content_type = ContentType.objects.get_for_model(get_user_model())
        permission = Permission.objects.get(
            codename = 'view_user',
            content_type = content_type,
        )

        self.user_logged_in.user_permissions.add(permission)
        self.user_logged_in.refresh_from_db()


class UserListGet(UserListWithPermission):
    def setUp(self):
        super(UserListGet, self).setUp()
        get_user_model().objects.create_user(
            username = 'user1',
            email = 'user1@domain.com',
            password = 'user1password',
            first_name = 'User',
            last_name = 'One'
        )
        get_user_model().objects.create_user(
            username = 'user2',
            email = 'user2@domain.com',
            password = 'user2password',
            first_name = 'User',
            last_name = 'Two'
        )
        self.response = self.client.get(r('accounts:user-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'accounts/user/list.html')

    def test_html(self):
        contents = [
            (1, 'User One'),
            (1, 'user1@domain.com'),
            (1, 'User Two'),
            (1, 'user2@domain.com'),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('accounts:user-create'))),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['users']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)