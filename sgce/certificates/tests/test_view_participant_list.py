from django.shortcuts import resolve_url as r

from sgce.certificates.models import Participant
from sgce.core.tests.base import LoggedInTestCase


class ParticipantListGet(LoggedInTestCase):
    def setUp(self):
        super(ParticipantListGet, self).setUp()
        Participant.objects.create(
            cpf='392.659.280-00',
            email='alan@turing.com',
            name='Alan Turing',
        )
        Participant.objects.create(
            cpf='740.690.920-99',
            email='barbara@liskov.com',
            name='Barbara Liskov',
        )
        self.response = self.client.get(r('certificates:participant-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/participant/participant_list.html')

    def test_html(self):
        contents = [
            (1, '392.659.280-00'),
            (1, 'alan@turing.com'),
            (1, 'Alan Turing'),
            (1, '740.690.920-99'),
            (1, 'barbara@liskov.com'),
            (1, 'Barbara Liskov'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['participants']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)