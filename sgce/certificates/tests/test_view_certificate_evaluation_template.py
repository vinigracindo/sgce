import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

from sgce.certificates.forms import CertificateEvaluationTemplateForm
from sgce.certificates.models import Template, Certificate, Participant, CertificateHistory
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class CertificateEvaluationTemplateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(CertificateEvaluationTemplateWithoutPermission, self).setUp()
        another_user = get_user_model().objects.create_user(username='another_user', password='password')
        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=another_user,
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
        self.response = self.client.get(r('certificates:certificates-evaluation-template', self.template.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Must be created by user logged in.
class CertificateEvaluationTemplateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(CertificateEvaluationTemplateWithPermission, self).setUp()
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=self.user_logged_in,
        )

        self.template = Template.objects.create(
            name='SBI - Certificado de Participante',
            event=self.event,
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


class CertificateEvaluationTemplateTest(CertificateEvaluationTemplateWithPermission):
    def setUp(self):
        super(CertificateEvaluationTemplateTest, self).setUp()
        self.response = self.client.get(r('certificates:certificates-evaluation-template', self.template.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/evaluation_template.html')

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, CertificateEvaluationTemplateForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class CertificateEvaluationTemplatePostTest(CertificateEvaluationTemplateWithPermission):
    def setUp(self):
        super(CertificateEvaluationTemplatePostTest, self).setUp()

        participant = Participant.objects.create(
            cpf='37377420812',
            email='alan@turing.com',
            name='Alan Turing',
        )

        participant2 = Participant.objects.create(
            cpf='07535867030',
            email='carol@shaw.com',
            name='Carol Shaw',
        )

        self.c1 = Certificate.objects.create(
            participant=participant,
            template=self.template,
        )

        self.c2 = Certificate.objects.create(
            participant=participant2,
            template=self.template,
            status=Certificate.VALID,
        )

        data = dict(
            notes='anything',
            status=Certificate.VALID,
            certificates=[self.c1.pk, self.c2.pk],
        )

        self.response = self.client.post(r('certificates:certificates-evaluation-template', self.template.pk), data)

        self.c1.refresh_from_db()
        self.c2.refresh_from_db()

    def test_post_certificate(self):
        """Must change certificate.status to Certificate.VALID"""
        self.assertEqual(self.c1.status, Certificate.VALID)
        self.assertEqual(self.c2.status, Certificate.VALID)

    def test_post_create_history(self):
        """Must create CertificateHistory instance for each change."""
        self.assertTrue(CertificateHistory.objects.exists())

    def test_post_should_not_create_history(self):
        """Should not create CertificateHistory instance for self.c2, because there was no change of status."""
        self.assertFalse(CertificateHistory.objects.filter(certificate=self.c2).exists())
