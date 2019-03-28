from django.urls import path

from . import views


urlpatterns = [
    path('add', views.add),
    path('get', views.get),
    path('set', views.set),
    path('touch', views.touch),
    path('delete', views.delete),
    path('get_many', views.get_many),
    path('get_or_set', views.get_or_set),
    path('has_key', views.has_key),
    path('incr', views.incr),
    path('decr', views.decr),
    path('set_many', views.set_many),
    path('delete_many', views.delete_many),
    path('clear', views.clear)
]
