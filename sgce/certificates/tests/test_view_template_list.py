from django.shortcuts import resolve_url as r

from model_mommy import mommy

from sgce.certificates.models import Template
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class TemplateListGet(LoggedInTestCase):
    def setUp(self):
        super(TemplateListGet, self).setUp()
        self.event = mommy.make(Event, created_by=self.user_logged_in)
        self.t1 = mommy.make(Template, event=self.event, background='core/tests/test.gif')
        self.t2 = mommy.make(Template, event=self.event, background='core/tests/test.gif')
        self.random_event = mommy.make(Template, event=mommy.make(Event), background='core/tests/test.gif')

        self.response = self.client.get(r('certificates:template-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/list.html')

    def test_html(self):
        contents = [
            (2, self.event.name),
            (1, self.t1.name),
            (1, self.t2.name),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['templates']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)

    def test_queryset(self):
        templates = self.response.context['templates']
        self.assertIn(self.t1, templates)
        self.assertIn(self.t2, templates)
        self.assertNotIn(self.random_event, templates)
