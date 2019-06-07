from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from sgce.accounts.forms import UserUpdateForm
from sgce.accounts.models import Profile


class UserUpdateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(UserUpdateWithoutPermission, self).setUp()
        self.response = self.client.get(r('accounts:user-update', self.user_logged_in.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Permission: auth.change_user and auth.view_user
class UserUpdateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(UserUpdateWithPermission, self).setUp()
        # permission required: profile.can_enable_or_disable_user
        content_type = ContentType.objects.get_for_model(get_user_model())
        p1 = Permission.objects.get(
            codename = 'change_user',
            content_type = content_type,
        )
        p2 = Permission.objects.get(
            codename = 'view_user',
            content_type = content_type,
        )

        self.user_logged_in.user_permissions.add(p1, p2)
        self.user_logged_in.refresh_from_db()


class UserUpdateGet(UserUpdateWithPermission):
    def setUp(self):
        super(UserUpdateGet, self).setUp()
        self.user_logged_in.first_name = 'Hello'
        self.user_logged_in.last_name = 'World'
        self.user_logged_in.email = 'hello@world.com'
        self.user_logged_in.save()

        self.response = self.client.get(r('accounts:user-update', self.user_logged_in.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'accounts/user/form.html')
        
    def test_inputs(self):
        """Html must contain filled inputs"""
        inputs = [
            'Hello', #first_name
            'World', #last_name
            'hello@world.com', #email
            'username', #username
        ]
        for input in inputs:
            with self.subTest():
                self.assertContains(self.response, 'value="{}"'.format(input))

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # Csrf, first_name, last_name, email, superuser and username
            ('<input', 6),
            ('type="text"', 3),
            ('type="checkbox"', 1),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, UserUpdateForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class UserUpdatePost(UserUpdateWithPermission):
    def setUp(self):
        super(UserUpdatePost, self).setUp()
        # user created on LoggedInTestCase setUp()
        data = dict(
            first_name = 'Alan',
            last_name = 'Turing',
            email = 'alan@turing.com',
            is_superuser = False,
            username = 'alanturing',
        )
        self.response = self.client.post(r('accounts:user-update', self.user_logged_in.pk), data)
        self.user_logged_in.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('accounts:user-list'))

    def test_update_user(self):
        self.assertEqual('Alan', self.user_logged_in.first_name)
        self.assertEqual('Turing', self.user_logged_in.last_name)
        self.assertEqual('alan@turing.com', self.user_logged_in.email)
        self.assertFalse(self.user_logged_in.is_superuser)
        self.assertEqual('alanturing', self.user_logged_in.username)