import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.forms import CertificateEvaluationTemplateForm
from sgce.certificates.models import Template, Certificate, Participant, CertificateHistory
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class CertificateHistoryWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(CertificateHistoryWithoutPermission, self).setUp()
        another_user = mommy.make(get_user_model())
        event = mommy.make(Event, created_by = another_user)
        template = mommy.make(Template, event = event, background = 'core/tests/teste.gif')
        participant = mommy.make(Participant)
        self.certificate = mommy.make(Certificate, participant = participant, template = template, fields = '')

        self.response = self.client.get(r('certificates:certificate-history', self.certificate.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Must be created by user logged in.
class CertificatHistoryTemplateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(CertificatHistoryTemplateWithPermission, self).setUp()
        event = mommy.make(Event, created_by = self.user_logged_in)
        template = mommy.make(Template, event = event, background = 'core/tests/teste.gif')
        participant = mommy.make(Participant)
        self.certificate = mommy.make(Certificate, participant = participant, template = template, fields = '')


class CertificateHistoryTemplateTest(CertificatHistoryTemplateWithPermission):
    def setUp(self):
        super(CertificateHistoryTemplateTest, self).setUp()

        mommy.make(CertificateHistory, certificate = self.certificate, notes = 'Log-entry-1')
        mommy.make(CertificateHistory, certificate = self.certificate, notes = 'Log-entry-2')
        mommy.make(CertificateHistory, certificate = self.certificate, notes = 'Log-entry-3')
        mommy.make(CertificateHistory, certificate = self.certificate, notes = 'Log-entry-4')
        mommy.make(CertificateHistory, certificate = self.certificate, notes = 'Log-entry-5')

        self.response = self.client.get(r('certificates:certificate-history', self.certificate.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/certificate/history.html')

    def test_html(self):
        contents = [
            'Log-entry-1',
            'Log-entry-2',
            'Log-entry-3',
            'Log-entry-4',
            'Log-entry-5',
        ]
        for log in contents:
            with self.subTest():
                self.assertContains(self.response, log)