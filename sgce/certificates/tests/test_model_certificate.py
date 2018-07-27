import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from sgce.certificates.models import Participant, Template, Certificate
from sgce.core.models import Event


class CertificateModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('user', 'user@mail.com', 'pass')

        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=user,
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

        self.participant = Participant.objects.create(
            cpf='373.774.208-12',
            email='alan@turing.com',
            name='Alan Turing',
        )

        self.certificate = Certificate.objects.create(
            participant=self.participant,
            template=self.template,
        )

    def test_create(self):
        self.assertTrue(Certificate.objects.exists())

    def test_str(self):
        self.assertEqual('Certificado de Alan Turing do modelo SBI - Certificado de Participante', str(self.certificate))

    def test_hash(self):
        self.assertTrue(len(self.certificate.hash) > 0)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            self.certificate = Certificate.objects.create(
                participant=self.participant,
                template=self.template,
            )


class CertificateManagerTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('user', 'user@mail.com', 'pass')

        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=user,
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

    def test_create_certificate(self):
        values = ['596.762.570-44', 'Alan Turing', 'Simpósio Internacional de Computação']
        Certificate.objects.create_certificate(self.template, values)
        self.assertTrue(Certificate.objects.exists())

    def test_invalid_cpf_create_certificate(self):
        values = ['111.111.111-11', 'Alan Turing', 'Simpósio Internacional de Computação']
        with self.assertRaises(ValidationError):
            Certificate.objects.create_certificate(self.template, values)