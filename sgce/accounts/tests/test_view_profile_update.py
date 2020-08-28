from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase
from sgce.accounts.forms import ProfileUpdateForm



class ProfileUpdateGet(LoggedInTestCase):
    def setUp(self):
        super(ProfileUpdateGet, self).setUp()
        self.user_logged_in.first_name = 'Hello'
        self.user_logged_in.last_name = 'World'
        self.user_logged_in.email = 'hello@world.com'
        self.user_logged_in.save()

        self.user_logged_in.refresh_from_db()

        self.response = self.client.get(r('accounts:profile-update'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'accounts/user/form.html')
        
    def test_inputs(self):
        """Html must contain filled inputs"""
        inputs = [
            'Hello', #first_name
            'World', #last_name
            'hello@world.com', #email
            'username', #username
        ]
        for input in inputs:
            with self.subTest():
                self.assertContains(self.response, 'value="{}"'.format(input))

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # Csrf, first_name, last_name, email, superuser and username
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_has_form(self):
        """Context must have user form"""
        form = self.response.context['form']
        self.assertIsInstance(form, ProfileUpdateForm)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ProfileUpdatePost(LoggedInTestCase):
    def setUp(self):
        super(ProfileUpdatePost, self).setUp()
        # user created on LoggedInTestCase setUp()
        data = dict(
            first_name='Alan',
            last_name='Turing',
            email='alan@turing.com',
            username='alanturing',
            password='ifal123456'
        )
        self.response = self.client.post(r('accounts:profile-update'), data)
        self.user_logged_in.refresh_from_db()

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('accounts:profile-update'))

    def test_update_user(self):
        self.assertEqual('Alan', self.user_logged_in.first_name)
        self.assertEqual('Turing', self.user_logged_in.last_name)
        self.assertEqual('alan@turing.com', self.user_logged_in.email)
        self.assertFalse(self.user_logged_in.is_superuser)
        self.assertEqual('alanturing', self.user_logged_in.username)
