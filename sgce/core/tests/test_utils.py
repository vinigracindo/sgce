from django.test import TestCase
from sgce.core.models import Event
from sgce.core.utils import slugify


class SlugifyTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            acronym='SBI',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
        )

    def test_create_event(self):
        """slug field should be 'simposio-brasileiro-de-informatica'"""
        self.assertEqual(self.event.slug, 'simposio-brasileiro-de-informatica')

    def test_edit_event(self):
        """slug should continue the same after editing"""
        self.event.location = 'IFAL - Campus Maceió'
        self.event.save()
        self.event.refresh_from_db()
        self.assertEqual(self.event.slug, 'simposio-brasileiro-de-informatica')

    def test_create_event_same_name(self):
        """slug field should be 'simposio-brasileiro-de-informatica-1'"""
        another_event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            acronym='SBI',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
        )
        self.assertEqual(another_event.slug, 'simposio-brasileiro-de-informatica-1')