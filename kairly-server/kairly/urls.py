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
from django.http import FileResponse
from django.urls import include, path
from django.views.static import serve
from django.views.generic.base import RedirectView

from corsheaders.middleware import CorsMiddleware


def serve_cors(request, *args, **kwargs):
    response = serve(request, *args, **kwargs)
    if isinstance(response, FileResponse):
        cmw = CorsMiddleware()
        return cmw.process_response(request, response)
    return response


def always_fail(request):
    raise ValueError("Calm down the endpoint always raise exception.")


urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('admin', RedirectView.as_view(url='admin/')),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('articles.urls')),
    path('api/fail', always_fail),
]

if settings.DEBUG:
    urlpatterns.extend(
        static('/media', view=serve_cors, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns.append(
        path('', RedirectView.as_view(url='http://localhost:3000'))
    )
