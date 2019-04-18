from django.test import TestCase
from accounts.models import User

class NoteModelTests(TestCase):
    def test_can_create_a_new_user(self):
            user = User.objects.create_user(username='not name', email='not@email.com',password="notpassword")
            self.assertTrue(user)

    def test_new_user_is_exist(self):
            user = User.objects.create_user(username='not name', email='not@email.com',password="notpassword")
            self.assertTrue(user == User.objects.last())

    def test_can_create_a_new_superuser(self):
            user = User.objects.create_superuser(username='not name', email='not@email.com',password="notpassword")
            self.assertTrue(user)

    def test_new_create_a_new_superuser_is_exist(self):
            user = User.objects.create_superuser(username='not name', email='not@email.com',password="notpassword")
            self.assertTrue(user==User.objects.last())