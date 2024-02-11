from django.urls import path

from . import views

app_name = 'coupon'

urlpatterns = [
    path('apply_coupon/', views.coupon_apply, name='apply_coupon'),
]
