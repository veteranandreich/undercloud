from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
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
        queryset = queryset.filter(owner=self.request.user)
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
        profile = get_object_or_404(self.get_queryset(), owner__pk=pk)
        user = profile.owner
        user.delete()
        return Response({"Status": "Delete completed"})

    def partial_update(self, request, pk=None, *args, **kwargs):
        profile = get_object_or_404(self.filter_queryset(self.queryset), owner__pk=pk)
        status = request.data.get("status", "Empty")
        about = request.data.get("about", "Empty")
        follow = request.data.get("follow", False)
        unfollow = request.data.get("unfollow", False)
        if status != "Empty":
            profile.status = status
        if about != "Empty":
            profile.about = about
        if follow and follow.isdigit() and follow != str(pk):
            profile.following.add(Profile.objects.get(pk=follow))
        if unfollow and unfollow.isdigit() and unfollow != str(pk):
            profile.following.remove(Profile.objects.get(pk=unfollow))
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method \"PUT\" not allowed."})


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
