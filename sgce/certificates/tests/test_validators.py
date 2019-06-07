import re

from django.core.exceptions import ValidationError
from django.test import TestCase
from sgce.certificates.validators import validate_cpf


class ValidateCPFTest(TestCase):
    def setUp(self):
        self.valid_inputs = [
            '501.938.580-88',
            '109.440.100-59',
            '381.991.790-07',
            '873.310.390-91',
            '311.186.100-75',

            '41675551073',
            '75023379035',
            '05818568059',
            '76450174064',
            '45149854069',
        ]

        self.invalid_numbers_inputs = [
            '000.000.000-00',
            '111.111.111-11',
            '222.222.222-22',
            '333.333.333-33',
            '444.444.444-44',
            '555.555.555-55',
            '666.666.666-66',
            '777.777.777-77',
            '888.888.888-88',
            '999.999.999-99',

            '00000000000',
            '11111111111',
            '22222222222',
            '33333333333',
            '44444444444',
            '55555555555',
            '66666666666',
            '77777777777',
            '88888888888',
            '99999999999',

            '12345678910',
            '15923654785',
        ]

        self.invalid_inputs = [
            'string',
            '123a567b910',
            'abcdefghijl',
        ]

    def test_cpf_is_valid(self):
        for cpf in self.valid_inputs:
            with self.subTest():
                # Remove '-' and '.'
                cpf = re.sub('[-\.]', '', cpf)
                self.assertEqual(cpf, validate_cpf(cpf))

        for cpf in self.invalid_numbers_inputs:
            with self.subTest():
                # Remove '-' and '.'
                cpf = re.sub('[-\.]', '', cpf)
                with self.assertRaisesMessage(ValidationError, 'Invalid CPF number'):
                    validate_cpf(cpf)

        for cpf in self.invalid_inputs:
            with self.subTest():
                # Remove '-' and '.'
                cpf = re.sub('[-\.]', '', cpf)
                with self.assertRaisesMessage(ValidationError, 'This field requires only numbers'):
                    validate_cpf(cpf)