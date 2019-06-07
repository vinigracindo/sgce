from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.models import Participant, Template, Certificate
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class CertificateListGet(LoggedInTestCase):
    def setUp(self):
        super(CertificateListGet, self).setUp()
        e1 = mommy.make(Event, created_by = self.user_logged_in)
        template = mommy.make(Template, event = e1, background = 'core/tests/test.gif')
        participant = mommy.make(Participant)
        self.certificate = mommy.make(Certificate, template = template, participant = participant, fields = '')

        another_user = mommy.make(get_user_model())
        e2 = mommy.make(Event, created_by = another_user)
        t2 = mommy.make(Template, event = e2, background = 'core/tests/test.gif')
        p2 = mommy.make(Participant)
        self.another_certificate = mommy.make(Certificate, template = t2, participant = p2, fields = '')

        self.response = self.client.get(r('certificates:certificate-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/certificate/list.html')

    def test_html(self):
        """Must show only certificate where certificate.template.event was created by user logged in."""
        self.assertContains(self.response, self.certificate.template.event.name)
        self.assertNotContains(self.response, self.another_certificate.template.event.name)

    def test_context(self):
        self.assertIn('certificates', self.response.context)


class CertificateListSuperUserGet(CertificateListGet):
    def setUp(self):
        super(CertificateListSuperUserGet, self).setUp()
        self.user_logged_in.is_superuser = True
        self.user_logged_in.save()
        self.user_logged_in.refresh_from_db()
        self.response = self.client.get(r('certificates:certificate-list'))

    def test_html(self):
        """Must show only certificate where certificate.template.event was created by user logged in."""
        self.assertContains(self.response, self.certificate.template.event.name)
        self.assertContains(self.response, self.another_certificate.template.event.name)