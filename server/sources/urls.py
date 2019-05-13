from django.urls import path

from . import views

urlpatterns = [
    path('import-rss', views.import_rss, name='import-rss'),
]