from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Edition


@login_required
def timeline(request):
    # editions = Edition.objects.filter(useredition__user=request.user)

    return JsonResponse({'ok': 1})
