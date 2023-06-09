from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateDataProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        labels = {
            'first_name': '',
            'last_name': '',
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }

