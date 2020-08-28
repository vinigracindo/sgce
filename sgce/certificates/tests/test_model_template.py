import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy

from sgce.certificates.models import Template
from sgce.core.models import Event


class TemplateModelTest(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(Event, created_by = user)

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
            has_qrcode=False,
            is_public=False,
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
        self.assertEqual('{}: {}'.format(self.template.event.name, self.template.name), str(self.template))

    def test_get_fields(self):
        self.assertListEqual(
            self.template.template_fields(),
            ['NUMERO_CPF', 'NOME_COMPLETO', 'NOME_EVENTO']
        )
        # another test
        self.template.content = '''
        O campo nome_evento não fará parte dos campos, pois está em lowercase.
        O campo NOME_EVENTO deve fazer parte.
        O campo NOME_COMPLETO também deve fazer parte.
        O CAMPO NOME_DO_EVENTO não deve fazer parte.
        ESTE_CAMPO_NAO_DEVE_FAZER_PARTE.
        EMAIL_PARTICIPANTE é um campo válido diferente de EMAIL_DO_PARTICIPANTE.
        Strings EM UPPER CASE SEM UNDERLINE NÃO DEVE FAZER PARTE.
        '''
        self.template.save()
        self.template.refresh_from_db()
        self.assertListEqual(
            self.template.template_fields(),
            ['NUMERO_CPF', 'NOME_COMPLETO', 'NOME_EVENTO', 'EMAIL_PARTICIPANTE']
        )

    def test_layout(self):
        """Default fields for layouts"""
        self.assertEqual(self.template.font, Template.ARIAL)
        self.assertEqual(self.template.title_top_distance, 3)
        self.assertEqual(self.template.title_section_align, Template.CENTER)
        self.assertEqual(self.template.title_align, Template.CENTER)
        self.assertEqual(self.template.title_color, Template.BLACK)
        self.assertEqual(self.template.title_font_size, 30)
        self.assertEqual(self.template.content_title_distance, 1)
        self.assertEqual(self.template.content_section_align, Template.CENTER)
        self.assertEqual(self.template.content_text_align, Template.JUSTIFY)
        self.assertEqual(self.template.content_text_color, Template.BLACK)
        self.assertEqual(self.template.content_font_size, 12)
        self.assertEqual(self.template.footer_title_distance, 0)
        self.assertEqual(self.template.footer_section_align, Template.CENTER)
        self.assertEqual(self.template.footer_text_align, Template.CENTER)
        self.assertEqual(self.template.footer_text_color, Template.BLACK)