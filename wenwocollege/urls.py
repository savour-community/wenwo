#encoding=utf-8

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'backoffice/', include('backoffice.urls')),
    path(r'v1/api/', include('frontend.api_v1.urls')),
    path(r'', include('frontend.urls')),
    path(r'ueditor', include('DjangoUeditor.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

