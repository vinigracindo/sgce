from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r
from sgce.core.forms import EventForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class EventCreateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(EventCreateWithoutPermission, self).setUp()
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            acronym='SBI',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
        )

        self.response = self.client.get(r('core:event-create'))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


#class Base. Add permission: add_event
class Base(LoggedInTestCase):
    def setUp(self):
        super(Base, self).setUp()
        # permission required: profile.can_enable_or_disable_user
        content_type = ContentType.objects.get_for_model(Event)
        self.permission = Permission.objects.get(
            codename='add_event',
            content_type=content_type,
        )

        self.user.user_permissions.add(self.permission)
        self.user.refresh_from_db()


class EventCreateGet(Base):
    def setUp(self):
        super(EventCreateGet, self).setUp()
        self.response = self.client.get(r('core:event-create'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/event_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # CSRF, Name, Acronym, Start_date, End_date and Location
            ('<input', 6),
            # Role
            ('type="text"', 5),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, EventForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#
# class UserCreatePost(Base):
#     def setUp(self):
#         super(UserCreatePost, self).setUp()
#         data = dict(
#             first_name = 'Alan',
#             last_name = 'Turing',
#             email = 'alan@turing.com',
#             is_superuser = False,
#             username = 'alanturing',
#             password = 'password',
#             role = Profile.MANAGER
#         )
#         self.response = self.client.post(r('accounts:user-create'), data)
#
#     def test_post(self):
#         """ Valid POST should redirect to 'user-list' """
#         self.assertRedirects(self.response, r('accounts:user-list'))
#
#     def test_save_user(self):
#         self.assertTrue(get_user_model().objects.filter(username='alanturing').exists())
#
#     def test_role_change_in_profile(self):
#         """
#         Must update profile.role attr. By default profile.role is 'u'.
#         When a user is created, a signal is triggered: create_user_profile (core/signals.py)
#         """
#         profile = get_user_model().objects.get(username='alanturing').profile
#         self.assertEqual(Profile.MANAGER, profile.role)
#
#
# class UserCreatePostInvalid(Base):
#     def setUp(self):
#         super(UserCreatePostInvalid, self).setUp()
#         self.response = self.client.post(r('accounts:user-create'), {})
#
#     def test_post(self):
#         """Invalid Post should not redirect"""
#         self.assertEqual(200, self.response.status_code)
#
#     def test_template(self):
#         self.assertTemplateUsed(self.response, 'accounts/user/user_form.html')
#
#     def test_has_form(self):
#         form = self.response.context['form']
#         self.assertIsInstance(form, UserForm)
#
#     def test_form_has_errors(self):
#         form = self.response.context['form']
#         self.assertTrue(form.errors)
#
#     def test_dont_save_new_user(self):
#         """The base class LoggedInTestCase creates a user."""
#         self.assertEqual(get_user_model().objects.exists(), 1)