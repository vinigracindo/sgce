import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy

from sgce.certificates.models import Participant, Template, Certificate, CertificateHistory
from sgce.core.models import Event


class CertificateHistoryModelTest(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(Event, created_by = user)
        template = mommy.make(Template, event = event, background = 'core/tests/test.gif')
        participant = mommy.make(Participant)
        certificate = Certificate.objects.create(
            participant = participant,
            template = template,
            fields = '',
            status = Certificate.PENDING,
        )

        self.certificate_history = CertificateHistory.objects.create(
            certificate = certificate,
            user = user,
            notes = 'anything',
            ip = '127.0.0.1',
        )

    def test_create(self):
        self.assertTrue(CertificateHistory.objects.exists())

    def test_str(self):
        self.assertEqual(
            '{} - {}'.format(self.certificate_history.certificate, self.certificate_history.user),
             str(self.certificate_history)
        )

    def test_created_at(self):
        """Template must have an auto created_at attr"""
        self.assertIsInstance(self.certificate_history.datetime, datetime.datetime)