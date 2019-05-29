import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from sgce.certificates.forms import TemplateDuplicateForm
from sgce.core.models import Event


class TemplateDuplicateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username = 'username', password = 'password')
        self.super_user = get_user_model().objects.create_superuser(
            username = 'another_user',
            email = 'email@gmail.com',
            password = 'password'
        )
        self.event1 = Event.objects.create(
            name = 'Simpósio Brasileiro de Informática',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user,
        )
        self.event2 = Event.objects.create(
            name = 'Simpósio Brasileiro de Medicina',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = self.super_user,
        )
        self.event3 = Event.objects.create(
            name = 'Simpósio Brasileiro de Engenharia',
            start_date = datetime.date(2018, 6, 18),
            end_date = datetime.date(2018, 6, 18),
            location = 'IFAL - Campus Arapiraca',
            created_by = self.user,
        )
        self.form = TemplateDuplicateForm(self.user)
        self.form_as_super_user = TemplateDuplicateForm(self.super_user)

    def test_form_has_fields(self):
        """Form must have one field"""
        expected = ['event']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_event_queryset(self):
        """The event queryset must show only events created by user OR all events if user is superuser"""
        self.assertEqual(
            set(list(self.form.fields['event'].queryset)),
            set([self.event1, self.event3])
        )

    def test_event_queryset_superuser(self):
        """must show all events case user is superuser"""
        self.assertEqual(
            set(list(self.form_as_super_user.fields['event'].queryset)),
            set([self.event1, self.event2, self.event3])
        )