from django.test import TestCase
from datetime import datetime
from sgce.core.models import Event
from django.shortcuts import resolve_url as r


class EventModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            acronym='SBI',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
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
        self.assertIsInstance(self.event.created_at, datetime)

    def test_get_absolute_url(self):
        url = r('core:event-detail', slug=self.event.slug)
        self.assertEqual(url, self.event.get_absolute_url())