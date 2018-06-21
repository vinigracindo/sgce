from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from sgce.core.models import Event


class EventListGet(LoggedInTestCase):
    def setUp(self):
        super(EventListGet, self).setUp()
        self.e1 = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            acronym='SBI',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
            #user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.e2 = Event.objects.create(
            name='Simpósio Brasileiro de Inteligência Artificial',
            acronym='SBIA',
            start_date='2018-06-19',
            end_date='2018-06-19',
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.response = self.client.get(r('core:event-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/event_list.html')

    def test_html(self):
        contents = [
            (1, 'Simpósio Brasileiro de Informática'),
            (1, '18 de Junho de 2018 a 18 de Junho de 2018'),
            (1, 'Simpósio Brasileiro de Inteligência Artificial'),
            (1, '19 de Junho de 2018 a 19 de Junho de 2018'),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:event-create'))),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
       variables = ['events']

       for key in variables:
           with self.subTest():
               self.assertIn(key, self.response.context)