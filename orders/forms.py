from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'postal_code', 'city']
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'address': '',
            'phone': '',
            'postal_code': '',
            'city': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Фамилия*'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Имя*'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email*'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес*'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон*'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Индекс*'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
