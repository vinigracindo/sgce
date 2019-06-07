from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.models import Participant
from sgce.core.tests.base import LoggedInTestCase


class ParticipantListGet(LoggedInTestCase):
    def setUp(self):
        super(ParticipantListGet, self).setUp()
        self.p1 = mommy.make(Participant, email = 'a@a.com')
        self.p2 = mommy.make(Participant, email = 'b@b.com')

        self.response = self.client.get(r('certificates:participant-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/participant/list.html')

    def test_html(self):
        contents = [
            (1, self.p1.name),
            (1, self.p1.email),
            (1, self.p1.cpf),
            (1, self.p2.name),
            (1, self.p2.email),
            (1, self.p2.cpf),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['participants']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)