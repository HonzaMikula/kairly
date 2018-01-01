from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/timeline', views.timeline, name='timeline'),
    path('api/profile', views.profile, name='profile'),
]
