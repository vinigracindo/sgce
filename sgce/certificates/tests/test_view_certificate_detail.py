from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.models import Template, Participant, Certificate
from sgce.core.models import Event


class CertificateDetailGet(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(Event, name = 'Simpósio Brasileiro de Informática', created_by = user)
        self.template = mommy.make(Template, event = event, background = 'core/tests/test.gif')
        participant = mommy.make(Participant, cpf = '67790155040')

        self.certificate = Certificate.objects.create(
            participant = participant,
            template = self.template,
            fields = '',
            status = Certificate.VALID,
        )
        self.response = self.client.get(r('certificates:certificate-detail', self.certificate.hash))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/certificate/detail.html')

    def test_context(self):
        variables = ['certificate']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)

    def test_html(self):
        contents = [
            self.certificate.participant.name,
            self.certificate.get_safe_content(),
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)


class CertificateDetailInvalidGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('certificates:certificate-detail', 'invalid-hash'))

    def test_get(self):
        self.assertContains(self.response, 'Certificado inválido')


class CertificateDetailTestInvalidStatusGet(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(Event, name = 'Simpósio Brasileiro de Informática', created_by = user)
        self.template = mommy.make(Template, event = event, background = 'core/tests/test.gif')
        participant = mommy.make(Participant, cpf = '67790155040')

        certificate = Certificate.objects.create(
            participant = participant,
            template = self.template,
            fields = '',
            status=Certificate.PENDING,
        )
        data = dict(
            hash = certificate.hash,
        )
        self.response = self.client.get(r('certificates:certificate-detail', certificate.hash))

    def test_error(self):
        self.assertContains(self.response, 'Certificado inválido')