from django.shortcuts import resolve_url as r
from sgce.core.tests.base import LoggedInTestCase


class IndexTest(LoggedInTestCase):
    def setUp(self):
        super(IndexTest, self).setUp()
        self.response = self.client.get(r('core:index'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'core/index.html')

    def test_html(self):
        contents = [
            'href="{}"'.format(r('core:index')),
            'href="{}"'.format(r('logout')),
        ]

        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)