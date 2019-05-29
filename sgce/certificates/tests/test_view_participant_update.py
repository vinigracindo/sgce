from django.shortcuts import resolve_url as r
from model_mommy import mommy

from sgce.certificates.forms import ParticipantForm
from sgce.certificates.models import Participant
from sgce.core.tests.base import LoggedInTestCase


class ParticipantUpdateWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(ParticipantUpdateWithoutPermission, self).setUp()
        self.participant = mommy.make(Participant)
        self.response = self.client.get(r('certificates:participant-update', self.participant.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


# Must be superuser.
class ParticipantUpdateWithPermission(LoggedInTestCase):
    def setUp(self):
        super(ParticipantUpdateWithPermission, self).setUp()

        self.participant = mommy.make(Participant, email = 'alan@turing.com')

        self.user_logged_in.is_superuser = True
        self.user_logged_in.save()
        self.user_logged_in.refresh_from_db()


class ParticipantUpdateGet(ParticipantUpdateWithPermission):
    def setUp(self):
        super(ParticipantUpdateGet, self).setUp()
        self.response = self.client.get(r('certificates:participant-update', self.participant.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'certificates/participant/form.html')

    def test_inputs(self):
        """Html must contain filled inputs"""
        inputs = [
            self.participant.name,
            self.participant.cpf,
            self.participant.email,
        ]
        for input in inputs:
            with self.subTest():
                self.assertContains(self.response, 'value="{}"'.format(input))

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # CSRF, Name, cpf and email
            ('<input', 4),
            ('type="text"', 2),
            ('type="email"', 1),
            ('type="hidden"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, ParticipantForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ParticipantUpdatePost(ParticipantUpdateWithPermission):
    def setUp(self):
        super(ParticipantUpdatePost, self).setUp()
        data = dict(
            name = 'User Name',
            cpf = '39265928000',
            email = 'user@name.com',
        )
        self.response = self.client.post(r('certificates:participant-update', self.participant.pk), data)
        self.participant.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('certificates:participant-list'))

    def test_update_user(self):
        self.assertEqual('User Name', self.participant.name)
        self.assertEqual('user@name.com', self.participant.email)
        self.assertEqual('39265928000', self.participant.cpf)