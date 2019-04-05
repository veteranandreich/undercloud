from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User, Audio


@login_required()
def feed(request):
    return render(request, 'profiles/feed.html', {'user': request.user.profile})


def page(request, pk):
    user = get_object_or_404(User, pk=pk)
    print(user)
    followers = user.profile.followers.all()
    following = user.profile.following.all()
    return render(request, 'profiles/profile.html',
                  {'profile': user.profile, 'followers': followers, 'following': following})


def upload(request):
    if request.method == "POST" and request.FILES['track']:
        audio = Audio(owner=request.user.profile, title=request.POST['title'], track=request.FILES['track'])
        print(audio)
        audio.save()
        return redirect('profiles:page', pk=request.user.pk)
    else:
        return render(request, 'profiles/upload.html')
