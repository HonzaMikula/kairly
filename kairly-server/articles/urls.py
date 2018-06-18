from django.urls import path, re_path

from . import views
from . import timeline

urlpatterns = [
    path('api/timeline', timeline.timeline, name='timeline'),

    path('api/editions', views.editions, name='editions'),
    path('api/editions/<author_id>/<slug:edition_slug>', views.edition, name='edition'),
    path('api/editions/<author_id>/<slug:edition_slug>/subscribe', views.subscribe, name='subscribe'),
    path('api/editions/<author_id>/<slug:edition_slug>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('api/editions/<author_id>/<slug:edition_slug>/backlog', views.edition_backlog, name='edition_backlog'),

    path('api/authors', views.authors, name='authors'),
    path('api/authors/<author_id>', views.author, name='author'),
    path('api/authors/<author_id>/posts', views.author_posts, name='author_posts'),
    path('api/authors/<author_id>/new-edition', views.create_edition, name='create_edition'),
    path('api/authors/<author_id>/subscribe', views.subscribe_author, name='subscribe_author'),
    path('api/authors/<author_id>/unsubscribe', views.unsubscribe_author, name='unsubscribe_author'),

    path('api/profile', views.profile, name='profile'),
    path('api/post/<int:post_id>', views.post, name='post'),

    # frontend paths, match anything
    re_path(r'', views.index, name='index'),
]
