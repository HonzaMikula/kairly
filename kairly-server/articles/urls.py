from django.urls import path

from . import views
from . import timeline

urlpatterns = [
    path('timeline', timeline.timeline, name='timeline'),

    path('editions', views.editions, name='editions'),
    path('editions/<author_id>/<slug:edition_slug>', views.edition, name='edition'),
    path('editions/<author_id>/<slug:edition_slug>/subscribe', views.subscribe, name='subscribe'),
    path('editions/<author_id>/<slug:edition_slug>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('editions/<author_id>/<slug:edition_slug>/backlog', views.edition_backlog, name='edition_backlog'),

    path('authors', views.authors, name='authors'),
    path('authors/<author_id>', views.author, name='author'),
    path('authors/<author_id>/posts', views.author_posts, name='author_posts'),
    path('authors/<author_id>/new-edition', views.create_edition, name='create_edition'),
    path('authors/<author_id>/subscribe', views.subscribe_author, name='subscribe_author'),
    path('authors/<author_id>/unsubscribe', views.unsubscribe_author, name='unsubscribe_author'),

    path('post/<int:post_id>', views.post, name='post'),
]
