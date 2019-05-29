from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.conf import settings


class LoginGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('login'))

    def test_get(self):
        """GET /login/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use accounts/login.html"""
        self.assertTemplateUsed(self.response, 'login.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 3),
                ('type="text"', 1),
                ('type="password"', 1),
                ('type="submit"', 1),
                ('method="post"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have login form"""
        form = self.response.context['form']
        self.assertIsInstance(form, AuthenticationForm)

    def test_form_has_fields(self):
        """form must have 2 fields (username and password)"""
        form = self.response.context['form']
        self.assertSequenceEqual(['username', 'password'], list(form.fields))

    def test_redirect_authenticated_user(self):
        """Must redirect to settings.LOGIN_REDIRECT_URL when user is authenticated."""
        get_user_model().objects.create_user(username = 'username', password = 'password')
        response = self.client.login(username = 'username', password = 'password')
        response = self.client.get(r('login'))
        self.assertRedirects(response, r(settings.LOGIN_REDIRECT_URL))


class LoginPostUserValid(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('usuario', 'usuario', 'userpass')
        data = dict(username=user.username, password = 'userpass')
        self.response = self.client.post(r('login'), data)

    def test_valid_user_redirect(self):
        """Valid POST should login user in session and redirect to /"""
        self.assertEqual(302, self.response.status_code)

    def test_user_is_authenticated(self):
        session = self.response.wsgi_request.session
        self.assertIn('_auth_user_id', session)


class LoginPostUserInvalid(TestCase):
    def setUp(self):
        data = dict(username='user_does_not_exist', password = 'anything')
        self.response = self.client.post(r('login'), data)

    def test_invalid_user_post(self):
        """Invalid Post should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_user_is_not_authenticated(self):
        session = self.response.wsgi_request.session
        self.assertNotIn('_auth_user_id', session)

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, AuthenticationForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_html(self):
        """HTML must contains error messages."""
        form = self.response.context['form']
        errors = form.non_field_errors()

        for error in errors:
            with self.subTest():
                self.assertContains(self.response, error)