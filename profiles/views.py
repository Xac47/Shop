from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from profiles.forms import UpdateDataProfileForm


@login_required
def my_profile(request):
    profile = request.user

    context = {
        'profile': profile,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def my_address(request):
    profile = request.user

    context = {
        'profile': profile,
    }

    return render(request, 'profiles/my_address.html', context)


@login_required
def my_orders(request):
    profile = request.user

    context = {
        'profile': profile,
    }

    return render(request, 'profiles/my_orders.html', context)

@login_required
def update_profile(request):
    profile = request.user
    form = UpdateDataProfileForm(instance=profile)

    if request.method == 'POST':
        form = UpdateDataProfileForm(request.POST, instance=profile)
        if form.is_valid():
            messages.success(request, 'Данные успешно обновлены')
            form.save()

    context = {
        'profile': profile,
        'form': form
    }

    return render(request, 'profiles/update_profile.html', context)