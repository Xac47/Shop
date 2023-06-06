from django.urls import path

from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('', views.my_profile, name='profile'),
]