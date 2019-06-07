from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.core.tests.base import LoggedInTestCase
from sgce.core.models import Event


class EventListGet(LoggedInTestCase):
    def setUp(self):
        super(EventListGet, self).setUp()
        self.another_user = mommy.make(get_user_model())

        self.e1 = mommy.make(Event, created_by = self.user_logged_in)
        self.e2 = mommy.make(Event, created_by = self.user_logged_in)
        self.e3 = mommy.make(Event, created_by = self.another_user)

        self.response = self.client.get(r('core:event-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/list.html')

    def test_html(self):
        """Must show only event created by user logged in."""
        contents_that_should_be_shown = [
            (1, self.e1.name),
            (1, self.e2.name),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:event-create'))),
        ]

        for count, expected in contents_that_should_be_shown:
            with self.subTest():
                self.assertContains(self.response, expected, count)

        contents_that_should_not_be_shown = [
            self.e3.name,
        ]

        for expected in contents_that_should_not_be_shown:
            with self.subTest():
                self.assertNotContains(self.response, expected)

    def test_context(self):
        variables = ['events']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)


class EventListSuperUserGet(EventListGet):
    def setUp(self):
        super(EventListSuperUserGet, self).setUp()
        self.user_logged_in.is_superuser = True
        self.user_logged_in.save()
        self.user_logged_in.refresh_from_db()
        self.response = self.client.get(r('core:event-list'))

    def test_html(self):
        """Must show alls events"""
        contents = [
            (1, self.e1.name),
            (1, self.e2.name),
            (1, self.e3.name),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:event-create'))),
        ]
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)