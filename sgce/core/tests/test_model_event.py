import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from sgce.core.models import Event
from django.shortcuts import resolve_url as r


class EventModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('user', 'user@mail.com', 'pass')
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=user,
        )

    def test_create(self):
        self.assertTrue(Event.objects.exists())

    def test_location_can_be_blank(self):
        field = Event._meta.get_field('location')
        self.assertTrue(field.blank)

    def test_str(self):
        self.assertEqual('Simpósio Brasileiro de Informática', str(self.event))

    def test_created_at(self):
        """Event must have an auto created_at attr"""
        self.assertIsInstance(self.event.created_at, datetime.datetime)

    def test_slug_cant_be_editable(self):
        """Event should not have an editable slug field."""
        field = Event._meta.get_field('slug')
        self.assertFalse(field.editable)

    def test_get_absolute_url(self):
        url = r('core:event-detail', slug=self.event.slug)
        self.assertEqual(url, self.event.get_absolute_url())