from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from . import views

from .views import ProfileViewSet

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('jwt-auth/', obtain_jwt_token),
    path('', include(router.urls)),
    path('register', views.CreateUserView.as_view(), name='register'),
    path('verify/', views.Verifier.as_view(), name='verifier'),
    path('upload/audio', views.UploadAudio.as_view(), name='audio_upload')
]