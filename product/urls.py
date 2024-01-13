from django.urls import path

from product import views

app_name = 'product'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('discounted_products/', views.DiscountProductListView.as_view(), name='discount_product'),

    path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category'),
    path('product/<slug:category_slug>/<int:pk>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add_review/<slug:product_slug>/', views.AddReviewProduct.as_view(), name='add_review'),

    path('products/favorites-list/', views.ProductFavoritesListView.as_view(), name='favorites_list'),
]
