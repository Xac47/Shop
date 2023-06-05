from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from account import views
from account.forms import PasswordResetForm, SetPasswordForm

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),

    path('password_reset/', PasswordResetView.as_view(form_class=PasswordResetForm), name='password_reset'),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(form_class=SetPasswordForm), name="password_reset_confirm"),

    path('', include('django.contrib.auth.urls')),

    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'),
         name='confirm_email'),

    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/',
         TemplateView.as_view(template_name='registration/invalid_verify.html'),
         name='invalid_verify'),

    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
]
