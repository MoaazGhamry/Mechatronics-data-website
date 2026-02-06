from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hub.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns += [
    path('manifest.json', serve, {'document_root': settings.STATIC_ROOT, 'path': 'manifest.json'}),
    path('sw.js', serve, {'document_root': settings.STATIC_ROOT, 'path': 'sw.js'}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
