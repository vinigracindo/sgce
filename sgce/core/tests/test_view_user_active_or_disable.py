from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from sgce.core.forms import UserForm
from sgce.core.models import Profile
from sgce.core.tests.base import LoggedInTestCase


class UserActiveOrDisable(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisable, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))

    def test_get(self):
        """Must redirect to core:user-list"""
        self.assertEqual(302, self.response.status_code)


class UserDisableGet(LoggedInTestCase):
    def setUp(self):
        super(UserDisableGet, self).setUp()
        self.user = get_user_model().objects.create_user(username='user_enable', password='password')
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_has_been_disabled(self):
        self.assertFalse(self.user.is_active)


class UserEnableGet(LoggedInTestCase):
    def setUp(self):
        super(UserEnableGet, self).setUp()
        self.user = get_user_model().objects.create_user(username='user_enable', password='password', is_active=False)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_has_been_enable(self):
        self.assertTrue(self.user.is_active)


class UserActiveOrDisableHimSelf(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisableHimSelf, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_wont_be_disabled(self):
        """The user cannot be himself."""
        self.assertTrue(self.user.is_active)