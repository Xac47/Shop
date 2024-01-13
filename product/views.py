import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, FormView

from product.forms import ReviewForm
from product.models import Product, Category, Reviews


class SearchView(ListView):
    """" Поиск Продуктов """""

    def get_queryset(self):
        return Product.published.filter(
            Q(category__slug=self.request.GET.get('category')) &
            Q(title__icontains=self.request.GET.get('q'))
            if self.request.GET.get('category')
            else Q(title__icontains=self.request.GET.get('q'))
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
    paginate_by = 10
    queryset = Product.published.all()


class ProductFavoritesListView(LoginRequiredMixin, ListView):
    """" Избранные товары """""
    template_name = 'product/favorites_list.html'

    def get_queryset(self):
        return self.request.user.favorites.all()


class ProductDetailView(DetailView):
    """" Товар """""
    extra_context = {
        'form': ReviewForm()
    }

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


class AddReviewProduct(LoginRequiredMixin, FormView):
    """" Отзыв под продуктом """""
    form_class = ReviewForm
    success_url = None

    def form_valid(self, form):
        product = Product.published.get(slug=self.kwargs['product_slug'])
        author = self.request.user
        Reviews.objects.update_or_create(
            product=product,
            author=author,
            defaults={
                'star': int(self.request.POST.get('star')),
                'message': str(self.request.POST.get('message')),
            }
        )
        self.success_url = product.get_absolute_url()
        return super().form_valid(form)
