import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class EventDetailWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(EventDetailWithoutPermission, self).setUp()
        another_user = get_user_model().objects.create_user(username = 'another_user', password = 'password')
        self.event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = another_user,
        )
        self.response = self.client.get(r('core:event-detail', self.event.slug))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Must be created by user logged in.
class EventDetailWithPermission(LoggedInTestCase):
    def setUp(self):
        super(EventDetailWithPermission, self).setUp()
        self.event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user_logged_in,
        )


class EventDetailGet(EventDetailWithPermission):
    def setUp(self):
        super(EventDetailGet, self).setUp()
        self.response = self.client.get(r('core:event-detail', self.event.slug))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/detail.html')

    def test_html(self):
        """Html must contain event attrs"""
        contents = [
            self.event.name,
        ]
        for text in contents:
            with self.subTest():
                self.assertContains(self.response, text)


class EventDetailInvalidGet(EventDetailWithPermission):
    def setUp(self):
        super(EventDetailInvalidGet, self).setUp()
        self.response = self.client.get(r('core:event-detail', 'event-does-not-exist'))

    def test_get(self):
        self.assertEqual(404, self.response.status_code)