from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from sgce.core.models import Event


class EventListGet(LoggedInTestCase):
    def setUp(self):
        super(EventListGet, self).setUp()
        another_user = get_user_model().objects.create_user('anotheruser', 'anotheruser@mail.com', 'pass')
        self.e1 = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
            #user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.e2 = Event.objects.create(
            name='Simpósio Brasileiro de Inteligência Artificial',
            start_date='2018-06-19',
            end_date='2018-06-19',
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.e3 = Event.objects.create(
            name='Simpósio Brasileiro de Medicina',
            start_date='2018-06-21',
            end_date='2018-06-21',
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=another_user,
        )
        self.response = self.client.get(r('core:event-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/event_list.html')

    def test_html(self):
        """Must show only event created by user logged in."""
        contents_that_should_be_shown = [
            (1, 'Simpósio Brasileiro de Informática'),
            (1, 'Simpósio Brasileiro de Inteligência Artificial'),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:event-create'))),
        ]

        for count, expected in contents_that_should_be_shown:
            with self.subTest():
                self.assertContains(self.response, expected, count)

        contents_that_should_not_be_shown = [
            'Simpósio Brasileiro de Medicina',
        ]

        for expected in contents_that_should_not_be_shown:
            with self.subTest():
                self.assertNotContains(self.response, expected)

    def test_context(self):
       variables = ['events']

       for key in variables:
           with self.subTest():
               self.assertIn(key, self.response.context)


class EventListSuperUserGet(LoggedInTestCase):
    def setUp(self):
        super(EventListSuperUserGet, self).setUp()
        self.user_logged_in.first_name = 'Grace'
        self.user_logged_in.last_name = 'Hopper'
        self.user_logged_in.is_superuser = True
        self.user_logged_in.save()
        self.user_logged_in.refresh_from_db()
        another_user = get_user_model().objects.create_user(
            username='anotheruser',
            email='anotheruser@mail.com',
            password='pass',
            first_name='Alan',
            last_name='Turing',
        )
        self.e1 = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date='2018-06-18',
            end_date='2018-06-18',
            location='IFAL - Campus Arapiraca',
            #user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.e2 = Event.objects.create(
            name='Simpósio Brasileiro de Inteligência Artificial',
            start_date='2018-06-19',
            end_date='2018-06-19',
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.e3 = Event.objects.create(
            name='Simpósio Brasileiro de Medicina',
            start_date='2018-06-21',
            end_date='2018-06-21',
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=another_user,
        )
        self.response = self.client.get(r('core:event-list'))

    def test_html(self):
        """Must show alls event and column created_by."""
        contents = [
            (1, 'Simpósio Brasileiro de Informática'),
            (1, 'Simpósio Brasileiro de Inteligência Artificial'),
            (1, 'Simpósio Brasileiro de Medicina'),
            (2, 'Grace Hopper'),
            (1, 'Alan Turing'),
            # Must have a link to create a new user.
            (1, 'href="{}"'.format(r('core:event-create'))),
        ]
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)