import datetime

from django.shortcuts import resolve_url as r

from sgce.certificates.forms import CertificateEvaluationForm
from sgce.certificates.models import Template
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class CertificatesEvaluationTest(LoggedInTestCase):
    def setUp(self):
        super(CertificatesEvaluationTest, self).setUp()
        self.response = self.client.get(r('certificates:certificates-evaluation'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/evaluation.html')

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, CertificateEvaluationForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class CertificatesEvaluationPostTest(LoggedInTestCase):
    def setUp(self):
        super(CertificatesEvaluationPostTest, self).setUp()
        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=self.user_logged_in,
        )

        self.template = Template.objects.create(
            name='SBI - Certificado de Participante',
            event=event,
            title='CERTIFICADO',
            content='''
                    Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO.
                    ''',
            backside_title='Programação',
            backside_content='''
                    1 - Abertura
                    2 - Lorem Ipsum
                    ''',
            background='core/tests/test.gif',
        )
        data = dict(
            event=event.pk,
            template=self.template.pk,
        )

        self.response = self.client.post(r('certificates:certificates-evaluation'), data)

    def test_post_status(self):
        self.assertEqual(302, self.response.status_code)

    def test_post(self):
        """ Valid POST should redirect to 'certificates-evaluation-template' """
        self.assertRedirects(self.response, r('certificates:certificates-evaluation-template', self.template.pk))

