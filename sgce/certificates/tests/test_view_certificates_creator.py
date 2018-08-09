import datetime

from django.shortcuts import resolve_url as r

from sgce.certificates.forms import CertificatesCreatorForm
from sgce.certificates.models import Template, Certificate, Participant
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class CertificatesCreatorGet(LoggedInTestCase):
    def setUp(self):
        super(CertificatesCreatorGet, self).setUp()
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
        self.response = self.client.get(r('certificates:certificates-creator'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, CertificatesCreatorForm)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/certificates_creator.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # csrf
            ('<input', 1),
            # template choices
            ('<select', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class CertificatesCreatorBlankDataPost(LoggedInTestCase):
    def setUp(self):
        super(CertificatesCreatorBlankDataPost, self).setUp()
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

        data = dict(
            template=self.template.pk,
            certificates='[]',
        )

        self.response = self.client.post(r('certificates:certificates-creator'), data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/certificates_creator.html')


class CertificatesCreatorPost(LoggedInTestCase):
    def setUp(self):
        super(CertificatesCreatorPost, self).setUp()
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

        data = dict(
            template=self.template.pk,
            certificates='[["181.144.390-76", "Alan Turing", "Evento"]]',
        )

        self.response = self.client.post(r('certificates:certificates-creator'), data)

    def test_template(self):
        """ Valid POST should render 'inspector.html' """
        self.assertTemplateUsed(self.response, 'certificates/template/inspector.html')

    def test_create_certificate(self):
        self.assertTrue(Certificate.objects.exists())

    def test_create_certificate_attrs(self):
        certificate = Certificate.objects.first()
        self.assertEqual("{'NOME_EVENTO': 'Evento'}", certificate.fields)

    def test_create_participant(self):
        self.assertTrue(Participant.objects.exists())

    def test_create_participant_attrs(self):
        participant = Participant.objects.first()
        self.assertEqual('18114439076', participant.cpf)
        self.assertEqual('Alan Turing', participant.name)


class CertificatesCreatorInvalidCpfPost(LoggedInTestCase):
    def setUp(self):
        super(CertificatesCreatorInvalidCpfPost, self).setUp()
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

        data = dict(
            template=self.template.pk,
            certificates='[["111.111.111-11", "Alan Turing", "Evento"]]',
        )

        self.response = self.client.post(r('certificates:certificates-creator'), data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/certificates_creator.html')

    def test_html_has_errors(self):
        self.assertContains(self.response, 'O CPF 111.111.111-11 da linha 1 é inválido.')


class CertificatesCreatorInvalidBlankValuesPost(LoggedInTestCase):
    def setUp(self):
        super(CertificatesCreatorInvalidBlankValuesPost, self).setUp()
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

        data = dict(
            template=self.template.pk,
            certificates='[["899.215.730-47", "", "Evento"]]',
        )

        self.response = self.client.post(r('certificates:certificates-creator'), data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/certificates_creator.html')

    def test_html_has_errors(self):
        self.assertContains(self.response, 'A tabela não pode conter valores em branco')

