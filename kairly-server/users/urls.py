from django.urls import path

from . import views


urlpatterns = [
    path('token', views.get_token),
    path('profile', views.profile, name='profile'),
]
