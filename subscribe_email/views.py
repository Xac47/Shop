from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from subscribe_email.forms import SubscribeEmailForm
from subscribe_email.models import SubscribeEmail


class AddSubscribeEmailView(CreateView):
    form_class = SubscribeEmailForm
    template_name = 'product/home_list.html'
    success_url = reverse_lazy('product:home')