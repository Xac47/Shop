from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_profile(request):
    profile = request.user

    context = {
        'profile': profile,
    }

    return render(request, 'profile/profile.html', context)
