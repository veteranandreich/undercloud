from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]
