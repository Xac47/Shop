from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as UserCreationFormDjango,
    UserChangeForm as UserChangeFormDjango
)
from django.core.exceptions import ValidationError

from .utils import send_email_for_verify

User = get_user_model()


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'E-mail'})
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
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
    email = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'placeholder': 'Password confirmation'}),
        strip=False,
    )

    class Meta(UserCreationFormDjango.Meta):
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeFormDjango):
    class Meta:
        model = User
        fields = ('email',)
