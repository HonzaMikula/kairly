from django.urls import path

from . import views


urlpatterns = [
    path('transactions', views.get_transactions),
    path('platform-transactions', views.get_platform_transactions),
]
