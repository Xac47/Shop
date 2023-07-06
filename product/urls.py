from django.urls import path

from product import views

app_name = 'product'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
]
