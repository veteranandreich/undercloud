from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Audio, Profile
from accounts.models import User

@login_required()
def feed(request):
    user = request.user
    followed_profiles = user.profile.following.all()
    audio_list = [audio for profile in followed_profiles for audio in profile.get_audio.all()]
    audio_list.sort(key=lambda audio: audio.publication_date, reverse=True)
    print(audio_list)
    return render(request, 'profiles/feed.html', {'audio': audio_list})


def page(request, pk):
    user = get_object_or_404(User, pk=pk)
    followers = user.profile.followers.all()
    following = user.profile.following.all()
    audio = user.profile.get_audio.all()
    return render(request, 'profiles/profile.html',
                  {'profile': user.profile, 'followers': followers, 'following': following, 'audio': audio})


@login_required()
def upload(request):
    if request.method == "POST" and request.FILES['track']:
        audio = Audio(owner=request.user.profile, title=request.POST['title'], track=request.FILES['track'])
        audio.save()
        return redirect('profiles:page', pk=request.user.pk)
    else:
        return render(request, 'profiles/upload.html')
