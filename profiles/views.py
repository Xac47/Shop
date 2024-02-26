from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from product.models import Product
from profiles.forms import UpdateDataProfileForm

User = get_user_model()


@login_required
def my_profile(request):
    profile = request.user

    context = {
        'profile': profile,
    }

    return render(request, 'profiles/profile.html', context)


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(SuccessMessageMixin, UpdateView):
    form_class = UpdateDataProfileForm
    template_name = 'profiles/update_profile.html'
    success_message = 'Данные успешно обновлены'
    success_url = reverse_lazy('profiles:update_profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def favorites_add_or_remove(request, product_id, product_slug):
    profile = request.user
    product = Product.published.get(id=product_id, slug=product_slug)
    if not profile.favorites.filter(id=product_id, slug=product_slug).exists():
        profile.favorites.add(product)
    else:
        profile.favorites.remove(product)

    return HttpResponseRedirect(
        request.META['HTTP_REFERER'])  # возвращает пользователя на ту страницу в котором он совершил данную операция
