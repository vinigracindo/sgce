import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.models import Template
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class TemplateDeleteWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(TemplateDeleteWithoutPermission, self).setUp()
        another_user = mommy.make(get_user_model())
        event = mommy.make(Event, created_by = another_user)
        self.template = mommy.make(Template, event = event, background = 'core/testes/test.gif')

        self.response = self.client.get(r('certificates:template-delete', self.template.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# template.event must be created by user logged in.
class TemplateDeleteWithPermission(LoggedInTestCase):
    def setUp(self):
        super(TemplateDeleteWithPermission, self).setUp()
        event = mommy.make(Event, created_by = self.user_logged_in)
        self.template = mommy.make(Template, event = event, background = 'core/testes/test.gif')


class TemplateDeleteGet(TemplateDeleteWithPermission):
    def setUp(self):
        super(TemplateDeleteGet, self).setUp()
        self.response = self.client.get(r('certificates:template-delete', self.template.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/delete.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            ('<input', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class TemplateDeletePost(TemplateDeleteWithPermission):
    def setUp(self):
        super(TemplateDeletePost, self).setUp()
        self.response = self.client.post(r('certificates:template-delete', self.template.pk))

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('certificates:template-list'))

    def test_save_user(self):
        self.assertFalse(Template.objects.exists())