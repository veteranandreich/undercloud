from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('feed', views.feed, name='feed'),
    path('<int:pk>', views.page, name='page'),
    path('upload', views.upload, name='upload'),
]
