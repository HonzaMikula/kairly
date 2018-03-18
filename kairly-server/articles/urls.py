from django.urls import path, re_path

from . import views

urlpatterns = [
    path('api/timeline', views.timeline, name='timeline'),
    path('api/editions', views.editions, name='editions'),
    path('api/editions/<slug:editor_slug>/<slug:edition_slug>', views.edition, name='edition'),
    path('api/subscribe/<slug:editor_slug>/<slug:edition_slug>', views.subscribe, name='subscribe'),
    path('api/subscribe/<slug:editor_slug>', views.subscribe_author, name='subscribe_author'),
    path('api/author/<slug:author_slug>', views.author, name='author'),
    path('api/profile', views.profile, name='profile'),
    path('api/post/<int:post_id>', views.post, name='post'),

    # frontend paths, match anything
    re_path(r'', views.index, name='index'),
]
