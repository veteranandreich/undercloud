from django.db import models
from accounts.models import User


def user_directory_path_audio(instance, filename):
    if Audio.objects.last():
        name = Audio.objects.last().pk+1
    else:
        name = 0
    return 'tracks/user_{0}/{1}'.format(instance.owner.owner.pk, name)


def user_directory_path_photo(instance, filename):
    return 'photos/user_{0}/{1}'.format(instance.owner.pk, instance.owner.pk)


class Profile(models.Model):
    owner = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path_photo, default='default.jpg')
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    status = models.CharField(max_length=134, blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.owner.username


class Audio(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='get_audio')
    title = models.CharField(max_length=16)
    track = models.FileField(upload_to=user_directory_path_audio, blank=False)
    publication_date = models.DateTimeField(auto_now_add=True)

