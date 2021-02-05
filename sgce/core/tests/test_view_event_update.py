import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

from sgce.core.forms import EventForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase
from sgce.accounts.models import Profile


class EventUpdateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(EventUpdateWithoutPermission, self).setUp()
        another_user = get_user_model().objects.create_user(username = 'another_user', password = 'password')
        self.event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = another_user,
        )
        self.response = self.client.get(r('core:event-update', self.event.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Must be created by user logged in.
class EventUpdateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(EventUpdateWithPermission, self).setUp()
        self.event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user_logged_in,
        )


class EventUpdateGet(EventUpdateWithPermission):
    def setUp(self):
        super(EventUpdateGet, self).setUp()
        self.response = self.client.get(r('core:event-update', self.event.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/form.html')

    def test_inputs(self):
        """Html must contain filled inputs"""
        inputs = [
            'Simpósio Brasileiro de Informática', #name
            '2018-06-18', #start_date
            '2018-06-18', #end_date
            'IFAL - Campus Arapiraca', #location
        ]
        for input in inputs:
            with self.subTest():
                self.assertContains(self.response, 'value="{}"'.format(input))

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


class EventUpdatePost(EventUpdateWithPermission):
    def setUp(self):
        super(EventUpdatePost, self).setUp()
        data = dict(
            name = 'Primeiro Encontro das Engenharias',
            start_date = datetime.date(2018, 7, 18),
            end_date = datetime.date(2018, 7, 18),
            location = 'Sesi',
            created_by = self.user_logged_in,
        )
        self.response = self.client.post(r('core:event-update', self.event.pk), data)
        self.event.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('core:event-list'))

    def test_update_user(self):
        self.assertEqual('Primeiro Encontro das Engenharias', self.event.name)
        self.assertEqual('primeiro-encontro-das-engenharias', self.event.slug)
        self.assertEqual(datetime.date(2018, 7, 18), self.event.start_date)
        self.assertEqual(datetime.date(2018, 7, 18), self.event.end_date)
        self.assertEqual('Sesi', self.event.location)