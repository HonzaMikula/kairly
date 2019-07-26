from django.urls import path

from . import views


urlpatterns = [
    path('token', views.get_token),
    path('refresh-token', views.refresh_token),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('signup', views.signup, name='signup'),
    path('change-password', views.change_password, name='change_password'),
    path('reset-password', views.reset_password, name='reset_password'),

    path('explore/<tab>', views.explore_tab),

    path('autocomplete/user/', views.UserAutocomplete.as_view(), name='user-autocomplete'),
    # path('query/user/', views.query_user, name="query-user"),
]
