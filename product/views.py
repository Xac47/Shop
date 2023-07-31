from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from product.models import Product, Category


class SearchView(ListView):
    """" Поиск Продуктов """""
    def get_queryset(self):
        return Product.published.filter(
            Q(category__name=self.request.GET.get('category')) |
            Q(title__icontains=self.request.GET.get('q'))
        )


class HomeListView(TemplateView):
    """" Главная страница """""
    template_name = 'product/home_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['popular_products'] = Product.published.all()[:10]
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductListView(ListView):
    """" Все Товары """""
    queryset = Product.published.all()


class ProductDetailView(DetailView):
    """" Товар """""
    def get_queryset(self):
        return Product.published.filter(id=self.kwargs['pk'],
                                        category__slug=self.kwargs['category_slug'],
                                        slug=self.kwargs['product_slug'])


class CategoryListView(ListView):
    """" Товары по категории """""
    template_name = 'product/category_list.html'

    def get_queryset(self):
        return Category.objects.get(slug=self.kwargs['category_slug']).product_set.all()
        # Product.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = Category.objects.get(slug=self.kwargs['category_slug']).name
        return ctx


class DiscountProductListView(ListView):
    """" Товары со скидками """""
    template_name = 'product/discount_product_list.html'

    def get_queryset(self):
        return Product.published.filter(discount__gte=1)
