from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('api/', include('api.urls', namespace='api'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
