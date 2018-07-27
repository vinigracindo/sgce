import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

from sgce.certificates.forms import TemplateForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase
from sgce.certificates.models import Template


class TemplateUpdateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(TemplateUpdateWithoutPermission, self).setUp()
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
        self.response = self.client.get(r('certificates:template-update', self.template.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Event must be created by user logged in for edit your templates.
class TemplateUpdateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(TemplateUpdateWithPermission, self).setUp()
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


class TemplateUpdateGet(TemplateUpdateWithPermission):
    def setUp(self):
        super(TemplateUpdateGet, self).setUp()
        self.response = self.client.get(r('certificates:template-update', self.template.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/template_form.html')

    def test_inputs(self):
        """Html must contain filled inputs"""
        inputs = [
            'SBI - Certificado de Participante',
            'Simpósio Brasileiro de Informática',
            'CERTIFICADO',
            'Certificamos que NOME_COMPLETO participou do evento NOME_EVENTO.',
            'Programação',
            '1 - Abertura',
            '2 - Lorem Ipsum',
            'core/tests/test.gif',
            Template.ARIAL,
            Template.LEFT,
            Template.BLACK,
        ]

        for input in inputs:
            with self.subTest():
                self.assertContains(self.response, input)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, TemplateForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class TemplateUpdatePost(TemplateUpdateWithPermission):
    def setUp(self):
        super(TemplateUpdatePost, self).setUp()
        data = dict(
            name='SBI - Certificado do Palestrante',
            event=self.event.pk,
            title='CERTIFICADO DE PALESTRANTE',
            content='''
                    Certificamos que NOME_COMPLETO apresentou a palestra NOME_PALESTRA no evento NOME_EVENTO.
                    ''',
            backside_title='Programação',
            backside_content='''
                    1 - Abertura
                    2 - Lorem Ipsum
                    ''',
            background='core/tests/test.gif',
            font=Template.ARIAL,
            title_top_distance=0,
            title_section_align=Template.LEFT,
            title_align=Template.LEFT,
            title_color=Template.BLACK,
            title_font_size=10,
            content_title_distance=0,
            content_section_align=Template.LEFT,
            content_text_align=Template.LEFT,
            content_text_color=Template.BLACK,
            content_font_size=10,
            footer_title_distance=0,
            footer_section_align=Template.LEFT,
            footer_text_align=Template.LEFT,
            footer_text_color=Template.BLACK,
        )
        self.response = self.client.post(r('certificates:template-update', self.template.pk), data)
        self.template.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('certificates:template-list'))

    def test_update_user(self):
        self.assertEqual('SBI - Certificado do Palestrante', self.template.name)
        self.assertEqual('CERTIFICADO DE PALESTRANTE', self.template.title)
        self.assertEqual('Certificamos que NOME_COMPLETO apresentou a palestra NOME_PALESTRA no evento NOME_EVENTO.', self.template.content)