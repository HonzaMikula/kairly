from django.urls import path

from . import views

urlpatterns = [
    path('api/timeline', views.timeline, name='timeline'),
    path('api/editions', views.editions, name='editions'),
    path('api/editions/<slug:editor_slug>/<slug:edition_slug>/subscribe', views.subscribe, name='subscribe'),
    path('api/profile', views.profile, name='profile'),
    path('api/post/<int:post_id>', views.post, name='post'),

    # frontend paths
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.index),
    path('editions', views.index),
    path('my-editions', views.index),
    path('read-later', views.index),
]
