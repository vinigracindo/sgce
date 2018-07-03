from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

import datetime
from sgce.certificates.models import Template
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class TemplateListGet(LoggedInTestCase):
    def setUp(self):
        super(TemplateListGet, self).setUp()
        event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )

        self.t1 = Template.objects.create(
            name='SBI - Certificado de Participante',
            event=event,
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
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )

        self.t2 = Template.objects.create(
            name='SBI - Certificado de Palestrante',
            event=event,
            title='CERTIFICADO',
            content='''
                            Certificamos que NOME_PARTICIPANTE palestrou no evento NOME_EVENTO.
                            ''',
            backside_title='Programação',
            backside_content='''
                            1 - Abertura
                            2 - Lorem Ipsum
                            ''',
            background='core/tests/test.gif',
            # user created on LoggedInTestCase setUp()
            created_by=self.user_logged_in,
        )
        self.response = self.client.get(r('certificates:template-list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/template/template_list.html')

    def test_html(self):
        contents = [
            (2, 'Simpósio Brasileiro de Informática'),
            (1, 'SBI - Certificado de Participante'),
            (1, 'SBI - Certificado de Palestrante'),
            # Must have a link to create a new user.
            #(1, 'href="{}"'.format(r('core:event-create'))),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['templates']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)