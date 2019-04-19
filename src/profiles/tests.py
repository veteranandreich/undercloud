from django.test import TestCase
from profiles.models import Profile, Audio
from accounts.models import User
import django


class NoteModelTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='not name', email='not@email.com', password="notpassword")
        profile = Profile(owner=User.objects.last())
        profile.save()

    def test_can_create_a_new_profile(self):
        profile = Profile(owner=User.objects.last())
        profile.save()
        self.assertTrue(profile)

    def test_profile_is_maked(self):
        profile = Profile(owner=User.objects.last())
        profile.save()
        self.assertTrue(profile == Profile.objects.last())

    def test_profile_audio_create(self):
        audio = Audio(owner=Profile.objects.last(), title="test.mp3", track="/test/audio.mp3")
        audio.save()
        self.assertTrue(audio)

    def test_profile_audio_is_maked(self):
        audio = Audio(owner=Profile.objects.last(), title="test.mp3", track="/test/audio.mp3")
        audio.save()
        self.assertTrue(audio == Audio.objects.last())

# Create your tests here.
