from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('', views.my_profile, name='profile'),
    path('my_address/', views.my_address, name='my_address'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('update/', views.update_profile, name='update_profile'),
]