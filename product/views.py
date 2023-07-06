from django.shortcuts import render
from django.views.generic import ListView

from product.models import Product



class HomeListView(ListView):
    queryset = Product.published.all()
    template_name = 'product/home_list.html'
