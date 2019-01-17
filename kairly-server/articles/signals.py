import django.dispatch

post_publish = django.dispatch.Signal(providing_args=["post"])
