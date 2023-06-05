from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as UserCreationFormDjango,
    UserChangeForm as UserChangeFormDjango,
    PasswordResetForm as PasswordResetFormDjango,
    SetPasswordForm as SetPasswordFormDjango,
)
from django.core.exceptions import ValidationError

from .utils import send_email_for_verify

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.EmailField(
        max_length=120,
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    password = forms.CharField(
        max_length=60,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )

    security_code = forms.CharField(
        label='',
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'Код безопасности*'})
    )
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache),
                raise ValidationError(
                    'Вы не подтвердили email, проверьте свою почту!',
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserCreationForm(UserCreationFormDjango):
    email = forms.EmailField(
        max_length=120,
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'unique': 'Этот Email уже зарегистрирован'}
    )
    password1 = forms.CharField(
        max_length=60,
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        max_length=60,
        label='',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Подтвердить пароль'}),
        strip=False,
    )
    security_code = forms.CharField(
        label='',
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'Код безопасности*'})
    )

    class Meta(UserCreationFormDjango.Meta):
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeFormDjango):
    class Meta:
        model = User
        fields = ('email',)


class PasswordResetForm(PasswordResetFormDjango):
    email = forms.EmailField(
        label=_("Email"),
        max_length=120,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'Email'}),
    )


class SetPasswordForm(SetPasswordFormDjango):
    new_password1 = forms.CharField(
        max_length=120,
        label=_(""),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Пароль*'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        max_length=120,
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Подтвердите свой пароль*'}),
    )