import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r

from sgce.accounts.models import Profile
from sgce.core.forms import EventForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class EventCreateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(EventCreateWithoutPermission, self).setUp()
        self.response = self.client.get(r('core:event-create'))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Permission: core.add_event
class EventCreateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(EventCreateWithPermission, self).setUp()
        # permission required: core.add_event
        content_type = ContentType.objects.get_for_model(Event)
        permission = Permission.objects.get(
            codename = 'add_event',
            content_type = content_type,
        )
        self.user_logged_in.user_permissions.add(permission)
        self.user_logged_in.refresh_from_db()


class EventCreateGet(EventCreateWithPermission):
    def setUp(self):
        super(EventCreateGet, self).setUp()
        self.response = self.client.get(r('core:event-create'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # CSRF, Name, Start_date, End_date and Location
            ('<input', 6),
            ('type="text"', 2),
            ('type="date"', 2),
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


class EventCreatePost(EventCreateWithPermission):
    def setUp(self):
        super(EventCreatePost, self).setUp()
        data = dict(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 21),
            end_date = datetime.date(2018, 6, 21),
            location = 'IFAL - Campus Arapiraca',
        )
        self.response = self.client.post(r('core:event-create'), data)

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('core:event-list'))

    def test_created_by_should_be_request_user(self):
        """obj.created_by should be request.user (user logged)."""
        obj = Event.objects.first()
        self.assertEqual(obj.created_by, self.user_logged_in)

    def test_save_user(self):
        self.assertTrue(Event.objects.exists())


class EventCreatePostInvalid(EventCreateWithPermission):
    def setUp(self):
        super(EventCreatePostInvalid, self).setUp()
        self.response = self.client.post(r('core:event-create'), {})

    def test_post(self):
        """Invalid Post should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, EventForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_new_user(self):
        self.assertFalse(Event.objects.exists())