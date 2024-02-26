from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('admin/order/<order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
]