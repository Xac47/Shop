from django import forms

from subscribe_email.models import SubscribeEmail


class SubscribeEmailForm(forms.ModelForm):
    class Meta:
        model = SubscribeEmail
        fields = ('email',)
        labels = {
            'email': ''
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your emaill address'})
        }
