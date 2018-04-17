from django.test import TestCase
from sgce.core.models import User


class LoggedInTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='username', password='password')
        self.client.login(username='username', password='password')