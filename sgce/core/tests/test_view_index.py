from django.test import TestCase
from django.shortcuts import resolve_url as r


class IndexTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('index'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'core/index.html')

    def test_menu_html(self):
        links = [
            'href="{}"'.format(r('user-list')),
        ]

        for link in links:
            with self.subTest():
                self.assertContains(self.response, link)

    def test_html(self):
        contents = [
            'href="{}"'.format(r('index')),
        ]

        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)