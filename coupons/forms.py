from django import forms

from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'font-medium mr-15 coupon', 'placeholder': 'Код купона'}))

    class Meta:
        fields = ('code',)