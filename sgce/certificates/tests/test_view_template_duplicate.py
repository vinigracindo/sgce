import datetime

from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.forms import TemplateForm, TemplateDuplicateForm
from sgce.certificates.models import Template
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class TemplateDuplicateGet(LoggedInTestCase):
    def setUp(self):
        super(TemplateDuplicateGet, self).setUp()
        event = mommy.make(Event, created_by = self.user_logged_in)
        self.template = mommy.make(Template, event = event, background = 'core/testes/test.gif')
        self.response = self.client.get(r('certificates:template-duplicate', self.template.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, TemplateDuplicateForm)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/duplicate.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # csrf
            ('<input', 1),
            # event choices
            ('<select', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class TemplateDuplicatePost(LoggedInTestCase):
    def setUp(self):
        super(TemplateDuplicatePost, self).setUp()
        self.e1 = mommy.make(Event, created_by = self.user_logged_in)
        self.e2 = mommy.make(Event, created_by = self.user_logged_in)

        self.template = Template.objects.create(
            name = 'SBI - Certificado de Participante',
            event = self.e1,
            title = 'CERTIFICADO',
            content = '''
                            Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO.
                            ''',
            backside_title = 'Programação',
            backside_content = '''
                            1 - Abertura
                            2 - Lorem Ipsum
                            ''',
            background = 'core/tests/test.gif',
        )

        data = dict(
            event = self.e2.pk
        )

        self.response = self.client.post(r('certificates:template-duplicate', self.template.pk), data)

    def test_redirect(self):
        """Must redirect to template-list"""
        self.assertRedirects(self.response, r('certificates:template-list'))

    def test_create(self):
        """Must create new Template"""
        self.assertEqual(Template.objects.count(), 2)

    def test_template_created(self):
        """The new template created must have the same attrs of self.template"""
        new_template = Template.objects.get(pk = 2)

        self.assertEqual(new_template.event, self.e2)

        self.assertEqual(self.template.name, new_template.name)
        self.assertEqual(self.template.title, new_template.title)
        self.assertEqual(self.template.content, new_template.content)
        self.assertEqual(self.template.backside_title, new_template.backside_title)
        self.assertEqual(self.template.backside_content, new_template.backside_content)
        self.assertEqual(self.template.background, new_template.background)
        self.assertEqual(self.template.font, new_template.font)
        self.assertEqual(self.template.title_top_distance, new_template.title_top_distance)
        self.assertEqual(self.template.title_section_align, new_template.title_section_align)
        self.assertEqual(self.template.title_align, new_template.title_align)
        self.assertEqual(self.template.title_color, new_template.title_color)
        self.assertEqual(self.template.title_font_size, new_template.title_font_size)
        self.assertEqual(self.template.content_title_distance, new_template.content_title_distance)
        self.assertEqual(self.template.content_section_align, new_template.content_section_align)
        self.assertEqual(self.template.content_text_align, new_template.content_text_align)
        self.assertEqual(self.template.content_text_color, new_template.content_text_color)
        self.assertEqual(self.template.content_font_size, new_template.content_font_size)
        self.assertEqual(self.template.footer_title_distance, new_template.footer_title_distance)
        self.assertEqual(self.template.footer_section_align, new_template.footer_section_align)
        self.assertEqual(self.template.footer_text_align, new_template.footer_text_align)
        self.assertEqual(self.template.footer_text_color, new_template.footer_text_color)

