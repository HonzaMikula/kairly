from django.urls import path

from . import views
from . import timeline

urlpatterns = [
    path('timeline', timeline.timeline, name='timeline'),

    path('recent/issues', views.recent_issues, name='recent_issues'),
    path('recent/posts', views.recent_posts, name='recent_posts'),
    path('newspapers/<username>/<slug:newspapeper_slug>', views.EditionView.as_view(), name='newspaper'),
    path('newspapers/<username>/<slug:newspapeper_slug>/subscribe', views.subscribe, name='subscribe'),
    path('newspapers/<username>/<slug:newspapeper_slug>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog', views.backlog, name='backlog'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog/publish', views.backlog_publish, name='backlog_publish'),

    path('authors/<username>', views.author, name='author'),
    path('authors/<username>/posts', views.author_posts, name='author_posts'),
    path('authors/<username>/start-newspaper', views.start_newspaper, name='start_newspaper'),
    path('authors/<username>/subscribe', views.subscribe_author, name='subscribe_author'),
    path('authors/<username>/unsubscribe', views.unsubscribe_author, name='unsubscribe_author'),

    path('post/<int:post_id>', views.post, name='post'),
]
