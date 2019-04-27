from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from profiles.models import Profile, Audio
from .serializers import ProfileSerializer, CreateUserSerializer, PostAudioSerializer, AudioSerializer
from accounts.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .pagination import FeedLimitPagination


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    pagination_class = FeedLimitPagination
    queryset = Profile.objects.all()

    def filter_queryset(self, queryset, *args, **kwargs):
        queryset = Profile.objects.filter(owner=self.request.user)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        profile = User.objects.get(pk=pk).profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        following_list = request.user.profile.following.all()
        audio_set = Audio.objects.filter(owner__in=following_list).order_by('-publication_date')
        page = self.paginate_queryset(audio_set)
        if page is not None:
            serializer = AudioSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AudioSerializer(audio_set, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response({"Error": "Profile already exist"})

    def destroy(self, request, pk=None, *args, **kwargs):
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
        profile = Profile(owner=user)
        profile.save()
        return Response({"Status": "Account verified"})


class UploadAudio(generics.CreateAPIView):
    model = Audio
    serializer_class = PostAudioSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)

