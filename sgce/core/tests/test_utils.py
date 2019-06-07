from django.contrib.auth import get_user_model
from django.test import TestCase
from sgce.core.models import Event


class SlugifyTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('user', 'user@mail.com', 'pass')
        self.event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = '2018-06-18',
            end_date = '2018-06-18',
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user,
        )

    def test_create_event(self):
        """slug field should be 'simposio-brasileiro-de-informatica'"""
        self.assertEqual(self.event.slug, 'simposio-brasileiro-de-informatica')

    def test_edit_event(self):
        """slug should continue the same if the name doesn't change after editing."""
        self.event.location = 'IFAL - Campus Maceió'
        self.event.save()
        self.event.refresh_from_db()
        self.assertEqual(self.event.slug, 'simposio-brasileiro-de-informatica')

    def test_edit_event_name(self):
        """slug should change if the name is changed."""
        self.event.name = 'II Simpósio Brasileiro de Informática'
        self.event.save()
        self.event.refresh_from_db()
        self.assertEqual(self.event.slug, 'ii-simposio-brasileiro-de-informatica')

    def test_create_event_same_name(self):
        """slug field should be 'simposio-brasileiro-de-informatica-1'"""
        another_event = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = '2018-06-18',
            end_date = '2018-06-18',
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user,
        )
        self.assertEqual(another_event.slug, 'simposio-brasileiro-de-informatica-1')