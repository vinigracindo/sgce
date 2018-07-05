import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import resolve_url as r

from sgce.accounts.models import Profile
from sgce.certificates.forms import TemplateForm
from sgce.certificates.models import Template
from sgce.core.forms import EventForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class TemplateCreateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(TemplateCreateWithoutPermission, self).setUp()
        self.response = self.client.get(r('certificates:template-create'))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


#class Base. Add user as MANAGER
class Base(LoggedInTestCase):
    def setUp(self):
        super(Base, self).setUp()
        # set as Profile.MANAGER
        self.user_logged_in.profile.role = Profile.MANAGER
        self.user_logged_in.profile.save()
        self.user_logged_in.profile.refresh_from_db()


class TemplateCreateGet(Base):
    def setUp(self):
        super(TemplateCreateGet, self).setUp()
        self.response = self.client.get(r('certificates:template-create'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/template_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 10),
            ('<select', 11),
            ('<textarea', 2),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, TemplateForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class TemplateCreatePost(Base):
    def setUp(self):
        super(TemplateCreatePost, self).setUp()
        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=self.user_logged_in,
        )

        data = dict(
            name='SBI - Certificado de Participante',
            event=event.pk,
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
        self.response = self.client.post(r('certificates:template-create'), data)

    def test_save_user(self):
        self.assertTrue(Template.objects.exists())

    def test_created_by_should_be_request_user(self):
        """obj.created_by should be request.user (user logged)."""
        obj = Template.objects.first()
        self.assertEqual(obj.created_by, self.user_logged_in)

    def test_post(self):
        """ Valid POST should redirect to 'template-list' """
        self.assertRedirects(self.response, r('certificates:template-list'))


class TemplateCreatePostInvalid(Base):
    def setUp(self):
        super(TemplateCreatePostInvalid, self).setUp()
        self.response = self.client.post(r('certificates:template-create'), {})

    def test_post(self):
        """Invalid Post should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/template_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, TemplateForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_new_user(self):
        self.assertFalse(Template.objects.exists())