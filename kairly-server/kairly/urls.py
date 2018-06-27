"""kairly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseNotFound


def index(request, *args, **kwargs):
    if request.path.startswith('/api') or request.path == '/favicon.ico':
        return HttpResponseNotFound()
    accept = request.META.get('HTTP_ACCEPT')
    if accept and 'text/html' not in accept:
        return HttpResponseBadRequest()

    return render(request, 'index.html')


urlpatterns = static('/media', document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin', RedirectView.as_view(url='admin/')),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('articles.urls')),

    # frontend paths, match anything, needs regexp!
    re_path(r'', index, name='index'),
]
