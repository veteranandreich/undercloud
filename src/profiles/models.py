from django.db import models
from accounts.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='default.jpg')
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    status = models.CharField(max_length=134)
    about = models.TextField()

    def __str__(self):
        return self.owner.username
