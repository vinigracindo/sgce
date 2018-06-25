import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from sgce.certificates.models import Template
from sgce.core.models import Event


class TemplateModelTest(TestCase):
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
            Certificamos que NOME_PARTICIPANTE participou do evento NOME_EVENTO.
            ''',
            backside_title='Programação',
            backside_content='''
            1 - Abertura
            2 - Lorem Ipsum
            ''',
            background='core/tests/test.gif',
            created_by=user,
        )

    def test_create(self):
        self.assertTrue(Template.objects.exists())

    def test_created_at(self):
        """Template must have an auto created_at attr"""
        self.assertIsInstance(self.template.created_at, datetime.datetime)

    def test_updated_at(self):
        """Template must have an auto updated_at attr"""
        self.assertIsInstance(self.template.updated_at, datetime.datetime)

    def test_title_can_be_blank(self):
        field = Template._meta.get_field('title')
        self.assertTrue(field.blank)

    def test_backside_title_can_be_blank(self):
        field = Template._meta.get_field('backside_title')
        self.assertTrue(field.blank)

    def test_backside_content_can_be_blank(self):
        field = Template._meta.get_field('backside_content')
        self.assertTrue(field.blank)

    def test_background_can_be_blank(self):
        field = Template._meta.get_field('background')
        self.assertTrue(field.blank)

    def test_str(self):
        self.assertEqual('SBI - Certificado de Participante', str(self.template))