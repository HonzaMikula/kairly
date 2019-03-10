from django.urls import path

from . import views
from . import timeline

urlpatterns = [
    path('timeline', timeline.timeline, name='timeline'),

    path('backlog', views.user_backlog, name='user_backlog'),
    path('subscriptions', views.subscriptions, name='subscriptions'),

    path('recent/issues', views.recent_issues, name='recent_issues'),
    path('recent/posts', views.recent_posts, name='recent_posts'),
    path('newspapers/<username>/<slug:newspapeper_slug>', views.NewspaperView.as_view(), name='newspaper'),
    path('newspapers/<username>/<slug:newspapeper_slug>/subscription', views.NewspaperSubscriptionView.as_view(), name='newspaper_subscribtion'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog', views.newspaper_backlog, name='newspaper_backlog'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog/publish', views.backlog_publish, name='backlog_publish'),

    path('authors/<username>', views.author, name='author'),
    path('authors/<username>/posts', views.author_posts, name='author_posts'),
    path('authors/<username>/start-newspaper', views.start_newspaper, name='start_newspaper'),
    path('authors/<username>/subscription', views.AuthorSubscriptionView.as_view(), name='author_subscription'),

    path('drafts', views.DraftsView.as_view(), name='drafts'),
    path('drafts/<int:post_id>', views.DraftDetailView.as_view(), name='draft'),
    path('drafts/<int:post_id>/publish', views.publish_draft, name='publish_draft'),
    path('posts/<username>/<post_slug>', views.post, name='post'),

    path('recommendation/post/<username>/<post_slug>', views.post_recommendation, name='post_recommendation'),
    path('recommendation/issue/<username>/<slug:newspapeper_slug>/<int:issue_number>', views.issue_recommendation, name='issue_recommendation'),
]
