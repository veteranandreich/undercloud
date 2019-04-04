from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('feed', views.feed, name='feed')
]
