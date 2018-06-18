from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r
from sgce.core.forms import UserUpdateForm
from sgce.core.models import Profile
from sgce.core.tests.base import LoggedInTestCase


class UserUpdateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(UserUpdateWithoutPermission, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)

        self.response = self.client.get(r('core:user-create'))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# class Base. Add permission: can_enable_or_disable_user
class Base(LoggedInTestCase):
    def setUp(self):
        super(Base, self).setUp()
        # permission required: profile.can_enable_or_disable_user
        content_type = ContentType.objects.get_for_model(get_user_model())
        self.permission = Permission.objects.get(
            codename='change_user',
            content_type=content_type,
        )

        self.user.user_permissions.add(self.permission)
        self.user.refresh_from_db()


class UserUpdateGet(Base):
    def setUp(self):
        super(UserUpdateGet, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        self.user.first_name = 'Hello'
        self.user.last_name = 'World'
        self.user.email = 'hello@world.com'
        self.user.save()

        self.response = self.client.get(r('core:user-update', self.user.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/user/user_form.html')
        
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
            # Role
            ('<select', 1),
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


class UserUpdatePost(Base):
    def setUp(self):
        super(UserUpdatePost, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        data = dict(
            first_name = 'Alan',
            last_name = 'Turing',
            email = 'alan@turing.com',
            is_superuser = False,
            username = 'alanturing',
            role = Profile.USER
        )
        self.response = self.client.post(r('core:user-update', self.user.pk), data)
        self.user.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('core:user-list'))

    def test_update_user(self):
        self.assertEqual('Alan', self.user.first_name)
        self.assertEqual('Turing', self.user.last_name)
        self.assertEqual('alan@turing.com', self.user.email)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual('alanturing', self.user.username)
        self.assertEqual(Profile.USER, self.user.profile.role)