from django.urls import path

from . import views
from . import timeline

urlpatterns = [
    path('timeline', timeline.TimelineView.as_view(), name='timeline'),
    path('explore-timeline/<tab>', timeline.ExploreTimelineView.as_view(), name="explore_timeline"),

    path('backlog', views.user_backlog, name='user_backlog'),
    path('subscriptions', views.subscriptions, name='subscriptions'),

    path('recent/issues', views.recent_issues, name='recent_issues'),
    path('recent/posts', views.recent_posts, name='recent_posts'),
    path('newspapers/<username>/<slug:newspapeper_slug>', views.NewspaperView.as_view(), name='newspaper'),
    path('newspapers/<username>/<slug:newspapeper_slug>/subscription', views.NewspaperSubscriptionView.as_view(), name='newspaper_subscribtion'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog', views.newspaper_backlog, name='newspaper_backlog'),
    path('newspapers/<username>/<slug:newspapeper_slug>/backlog/links', views.create_link, name='create_link'),

    path('authors/<username>', views.author_detail, name='author'),
    path('authors/<username>/posts', views.author_posts, name='author_posts'),
    path('authors/<username>/start-newspaper', views.start_newspaper, name='start_newspaper'),
    path('authors/<username>/subscription', views.AuthorSubscriptionView.as_view(), name='author_subscription'),

    path('drafts', views.DraftsView.as_view(), name='drafts'),
    path('drafts/<int:post_id>', views.DraftDetailView.as_view(), name='draft'),
    path('drafts/<int:post_id>/fair-price', views.draft_fair_price, name='draft_fair_prace'),
    path('drafts/<int:post_id>/publish', views.publish_draft, name='publish_draft'),
    path('posts/<username>/<post_slug>', views.post, name='post'),

    path('recommendation/post/<username>/<post_slug>', views.PostRecommendationView.as_view(), name='post_recommendation'),
    path('recommendation/issue/<username>/<slug:newspapeper_slug>/<int:issue_number>', views.IssueRecommendationView.as_view(), name='issue_recommendation'),

    path('p', views.media_proxy, name='media_proxy'),
]
