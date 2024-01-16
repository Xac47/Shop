from django.urls import path

from . import views

app_name = 'subscribe_email'

urlpatterns = [
    path('add/', views.AddSubscribeEmailView.as_view(), name='add_subscribe_email'),
]