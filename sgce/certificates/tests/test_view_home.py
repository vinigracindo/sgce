from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from sgce.certificates.forms import HomeForm
from sgce.certificates.models import Certificate, Participant, Template
from sgce.core.models import Event


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'home.html')

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, HomeForm)


class HomeTestPost(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(
            Event, name='Simpósio Brasileiro de Informática', created_by=user)
        self.template = mommy.make(
            Template, event=event, background='core/tests/test.gif')
        participant = mommy.make(Participant, dni='67790155040')

        self.certificate = Certificate.objects.create(
            participant=participant,
            template=self.template,
            fields='',
            status=Certificate.VALID,
        )
        data = dict(
            dni='67790155040',
        )
        self.response = self.client.post(r('home'), data)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'home.html')

    def test_context(self):
        variables = ['certificates']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)

    def test_html(self):
        Certificate.objects.create(
            participant=mommy.make(Participant, dni='07298801090'),
            template=self.template,
            fields='',
            status=Certificate.VALID,
        )

        contents = [
            (1, '67790155040'),
            (0, '07298801090'),
            (1, 'Simpósio Brasileiro de Informática'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_error(self):
        data = dict(
            dni='376.727.930-47',
        )
        self.response = self.client.post(r('home'), data)

        self.assertContains(
            self.response, 'Não existem certificados válidos para este DNI.')
