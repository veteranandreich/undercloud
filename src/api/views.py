from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from profiles.models import Profile, Audio
from .serializers import ProfileSerializer, CreateUserSerializer, AudioSerializer
from accounts.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def filter_queryset(self, queryset):
        queryset = Profile.objects.filter(owner=self.request.user)
        return queryset

    def retrieve(self, request, pk=None):
        profile = User.objects.get(pk=pk).profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def list(self, request):
        user = Profile.objects.filter(owner=request.user).get()
        queryset = user.following.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        return Response({"Error": "Profile already exist"})

    def destroy(self, request, pk=None):
        profile = get_object_or_404(Profile, pk=pk, owner=request.user)
        user = profile.owner
        user.delete()
        return Response({"Status": "Delete completed"})


class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer


class Verifier(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        pk = request.GET.get("pk")
        token = request.GET.get("token")
        user = User.objects.filter(pk=pk).get()
        if str(user.token) == str(token):
            user.is_active = True
        user.save()
        return Response({"Status": "Account verified"})

# Rewrtie to viewset
class UploadAudio(generics.CreateAPIView):
    model = Audio
    serializer_class = AudioSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)

