from django.test import TestCase
from sgce.certificates.models import Participant


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            dni='37377420812',
            email='alan@turing.com',
            name='Alan Turing',
        )

    def test_create(self):
        self.assertTrue(Participant.objects.exists())

    def test_email_can_be_blank(self):
        field = Participant._meta.get_field('email')
        self.assertTrue(field.blank)

    def test_str(self):
        self.assertEqual('Alan Turing (37377420812)', str(self.participant))
