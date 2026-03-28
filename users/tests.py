from django.test import TestCase
from django.contrib.auth.models import User


class UserTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(username="testuser", password="12345")
        self.assertEqual(user.username, "testuser")