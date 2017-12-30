from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import views
from django.shortcuts import render
from django.http import JsonResponse

from .models import Edition


def index(request):
    return render(request, 'index.html')


@login_required
def timeline(request):
    # editions = Edition.objects.filter(useredition__user=request.user)

    return JsonResponse({'ok': 1})
