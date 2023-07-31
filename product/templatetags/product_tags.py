from django import template
from django.db.models import Count

from product.models import Category, Product

register = template.Library()


@register.inclusion_tag('product/tags/categories.html')
def categories():
    start_categories = Category.objects.all()[:11]
    end_categories = Category.objects.all()[11:]
    return {
        'start_categories': start_categories,
        'end_categories': end_categories
    }


@register.simple_tag
def search_categories():
    return Category.objects.all()


@register.inclusion_tag('product/tags/deals_of_the_day.html')
def discount_products():
    products = Product.published.filter(
        discount__gte=1
    )
    return {
        'products': products
    }


@register.simple_tag
def get_similar_products(product):
    post_tags = product.tags.values_list('id', flat=True)
    similar_products = Product.published.filter(category=product.category, tags__in=post_tags).exclude(id=product.id)
    return similar_products.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
