from django.urls import path, re_path

from . import views
from . import timeline

urlpatterns = [
    path('api/timeline', timeline.timeline, name='timeline'),
    path('api/editions', views.editions, name='editions'),
    path('api/authors', views.authors, name='authors'),
    path('api/editions/<author_id>/<slug:edition_slug>', views.edition, name='edition'),
    path('api/subscribe/<author_id>/<slug:edition_slug>', views.subscribe, name='subscribe'),
    path('api/unsubscribe/<author_id>/<slug:edition_slug>', views.unsubscribe, name='unsubscribe'),
    path('api/subscribe/<author_id>', views.subscribe_author, name='subscribe_author'),
    path('api/unsubscribe/<author_id>', views.unsubscribe_author, name='unsubscribe_author'),
    path('api/author/<author_id>', views.author, name='author'),
    path('api/author/<author_id>/posts', views.author_posts, name='author_posts'),
    path('api/profile', views.profile, name='profile'),
    path('api/post/<int:post_id>', views.post, name='post'),

    # frontend paths, match anything
    re_path(r'', views.index, name='index'),
]
