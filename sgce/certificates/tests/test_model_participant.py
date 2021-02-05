from django.test import TestCase
from sgce.certificates.models import Participant
from sgce.certificates.validators import validate_cpf


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            cpf = '37377420812',
            email = 'alan@turing.com',
            name = 'Alan Turing',
        )

    def test_create(self):
        self.assertTrue(Participant.objects.exists())

    def test_email_can_be_blank(self):
        field = Participant._meta.get_field('email')
        self.assertTrue(field.blank)



    def test_str(self):
        self.assertEqual('Alan Turing (373.774.208-12)', str(self.participant))

    def test_cpf_must_contains_cpf_validator(self):
        field = Participant._meta.get_field('cpf')
        self.assertTrue(validate_cpf in field.validators)