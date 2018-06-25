from django.urls import path

from . import views
from . import timeline

urlpatterns = [
    path('timeline', timeline.timeline, name='timeline'),

    path('user/editions', views.user_editions, name='user_editions'),
    path('editions/<username>/<slug:edition_slug>', views.edition, name='edition'),
    path('editions/<username>/<slug:edition_slug>/subscribe', views.subscribe, name='subscribe'),
    path('editions/<username>/<slug:edition_slug>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('editions/<username>/<slug:edition_slug>/backlog', views.edition_backlog, name='edition_backlog'),

    path('user/authors', views.user_authors, name='user_authors'),
    path('authors/<username>', views.author, name='author'),
    path('authors/<username>/posts', views.author_posts, name='author_posts'),
    path('authors/<username>/new-edition', views.create_edition, name='create_edition'),
    path('authors/<username>/subscribe', views.subscribe_author, name='subscribe_author'),
    path('authors/<username>/unsubscribe', views.unsubscribe_author, name='unsubscribe_author'),

    path('post/<int:post_id>', views.post, name='post'),
]
