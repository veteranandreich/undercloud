from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def feed(request):
    username = request.user.username
    return render(request, 'profiles/feed.html', {'username': username})
