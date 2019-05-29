from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.core.tests.base import LoggedInTestCase


class UserActiveOrDisableWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisableWithoutPermission, self).setUp()
        self.response = self.client.get(r('accounts:user-active-or-disable', self.user_logged_in.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Permission: auth.delete_user
class UserActiveOrDisableWithPermission(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisableWithPermission, self).setUp()
        # permission required: profile.can_enable_or_disable_user
        content_type = ContentType.objects.get_for_model(get_user_model())
        permission = Permission.objects.get(
            codename = 'delete_user',
            content_type = content_type,
        )

        self.user_logged_in.user_permissions.add(permission)
        self.user_logged_in.refresh_from_db()


class UserActiveOrDisable(UserActiveOrDisableWithPermission):
    def setUp(self):
        super(UserActiveOrDisable, self).setUp()
        another_user = mommy.make(get_user_model())
        self.response = self.client.get(r('accounts:user-active-or-disable', another_user.pk))

    def test_get(self):
        """Must redirect to accounts:user-list"""
        self.assertEqual(302, self.response.status_code)


class UserDisableGet(UserActiveOrDisableWithPermission):
    def setUp(self):
        super(UserDisableGet, self).setUp()
        self.another_user = mommy.make(get_user_model(), is_active = True)
        self.response = self.client.get(r('accounts:user-active-or-disable', self.another_user.pk))
        self.another_user.refresh_from_db()

    def test_user_has_been_disabled(self):
        self.assertFalse(self.another_user.is_active)


class UserEnableGet(UserActiveOrDisableWithPermission):
    def setUp(self):
        super(UserEnableGet, self).setUp()
        self.another_user = mommy.make(get_user_model(), is_active = False)
        self.response = self.client.get(r('accounts:user-active-or-disable', self.another_user.pk))
        self.another_user.refresh_from_db()

    def test_user_has_been_enable(self):
        self.assertTrue(self.another_user.is_active)


class UserActiveOrDisableHimSelf(UserActiveOrDisableWithPermission):
    def setUp(self):
        super(UserActiveOrDisableHimSelf, self).setUp()
        self.response = self.client.get(r('accounts:user-active-or-disable', self.user_logged_in.pk))
        self.user_logged_in.refresh_from_db()

    def test_user_wont_be_disabled(self):
        """The user cannot be himself."""
        self.assertTrue(self.user_logged_in.is_active)