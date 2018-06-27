from django.urls import path

from . import views


urlpatterns = [
    path('token', views.get_token),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('signup', views.signup, name='signup'),
]
