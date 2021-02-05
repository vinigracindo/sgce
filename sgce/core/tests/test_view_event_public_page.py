import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.core.models import Event


class EventPublicPageGet(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        self.event = mommy.make(Event, created_by=user)
        self.response = self.client.get(r('event-public-page', self.event.slug))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/public.html')

    def test_context(self):
        variables = ['event']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)

    def test_html(self):
        """Html must contain event attrs"""
        contents = [
            self.event.name,
        ]
        for text in contents:
            with self.subTest():
                self.assertContains(self.response, text)
