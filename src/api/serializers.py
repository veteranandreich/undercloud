from rest_framework import serializers
from profiles.models import Profile, Audio
from accounts.models import User
from django.core.mail import send_mail
from main.settings import EMAIL_HOST_USER
import random
import string


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_of_registration', 'is_active')


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def generate_token(self):
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(64))

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        token = self.generate_token()
        user.token = token
        user.save()
        text = f"""Please confirm your registration via this link 127.0.0.1:8000/api/verify/?pk={user.pk}&token={token}. If you didn't sign up for our site just ignore this letter"""
        send_mail('Undercloud verification', text, from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email], fail_silently=True)

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FollowersSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Profile
        fields = ('owner',)


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('owner', 'title', 'track', 'publication_date')


class ProfileSerializer(serializers.ModelSerializer):

    owner = UserSerializer()
    get_audio = AudioSerializer(many=True)
    followers = FollowersSerializer(many=True)
    following = FollowersSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('owner', 'photo', 'followers', 'following', 'get_audio', 'status', 'about')


class FollowingSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    get_audio = AudioSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('owner', 'get_audio')
