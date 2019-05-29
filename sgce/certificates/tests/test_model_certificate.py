import datetime

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from sgce.certificates.models import Participant, Template, Certificate
from sgce.core.models import Event


class CertificateModelTest(TestCase):
    def setUp(self):
        user = mommy.make(get_user_model())
        event = mommy.make(Event, created_by = user)
        self.template = mommy.make(Template, event = event, background = 'core/tests/test.gif')
        self.participant = mommy.make(Participant)

        self.certificate = Certificate.objects.create(
            participant = self.participant,
            template = self.template,
            fields = '',
            status = Certificate.PENDING,
        )

    def test_create(self):
        self.assertTrue(Certificate.objects.exists())

    def test_created_at(self):
        """Template must have an auto created_at attr"""
        self.assertIsInstance(self.certificate.created_at, datetime.datetime)

    def test_str(self):
        self.assertEqual('Certificado de {} do modelo {}'.format(self.certificate.participant.name,
                                                                 self.certificate.template.name), str(self.certificate))

    def test_hash(self):
        self.assertTrue(len(self.certificate.hash) > 0)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            self.certificate = Certificate.objects.create(
                participant = self.participant,
                template = self.template,
            )
