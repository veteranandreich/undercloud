from django.test import TestCase
from accounts.models import User

class NoteModelTests(TestCase):
    def test_can_create_a_new_user(self):
            user = User.objects.create(username='not name', email='not@email.com',password="notpassword")
            self.assertTrue(user)
