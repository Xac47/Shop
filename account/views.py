from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, \
    PasswordChangeView as PasswordChangeViewDjango
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView

from .forms import UserCreationForm, AuthenticationForm, ChangeEmailForm
from django.shortcuts import render, redirect
from django.views import View

from .utils import send_email_for_verify, security_code

User = get_user_model()


class MyLoginView(LoginView):
    form_class = AuthenticationForm


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('profiles:profile')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class SignUpView(View):
    template_name = 'registration/sign_up.html'

    def get(self, request):
        code = security_code()
        globals()['code'] = code
        context = {
            'form': UserCreationForm(),
            'security_code': list(code)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            code = globals()['code']
        except KeyError:
            code = None

        form = UserCreationForm(request.POST)

        """ Проверка кода безопасности """
        if not code == request.POST.get('security_code'):
            messages.error(self.request, 'Не правильный код')
            context = {
                'form': UserCreationForm(),
            }
            context['security_code'] = globals()['code'] = security_code()
            return render(request, self.template_name, context)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')

        context = {
            'form': form,
        }
        context['security_code'] = globals()['code'] = security_code()
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class PasswordChangeView(SuccessMessageMixin, PasswordChangeViewDjango):
    success_url = reverse_lazy('password_change')
    success_message = 'Пароль успешно изменен'


@method_decorator(login_required, name='dispatch')
class ChangeEmailView(SuccessMessageMixin, UpdateView):
    form_class = ChangeEmailForm
    template_name = 'registration/change_email.html'
    success_message = 'Email успешно изменен'
    success_url = reverse_lazy('change_email')

    def get_object(self, queryset=None):
        return self.request.user
