from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.forms import CertificateValidateForm
from sgce.certificates.models import Template, Participant, Certificate
from sgce.core.models import Event


class CertificateValidateTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('certificates:certificate-validate'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use certificates/certificate/validate.html"""
        self.assertTemplateUsed(self.response, 'certificates/certificate/validate.html')

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, CertificateValidateForm)


class CertificateValidateTestPost(TestCase):
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
        data = dict(
            hash = self.certificate.hash,
        )
        self.response = self.client.post(r('certificates:certificate-validate'), data)

    def test_post_status(self):
        self.assertEqual(302, self.response.status_code)

    def test_post(self):
        """ Valid POST should redirect to 'certificates-evaluation-template' """
        self.assertRedirects(self.response, r('certificates:certificate-detail', self.certificate.hash))