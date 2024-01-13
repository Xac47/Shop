from django import forms

from product.models import Reviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ('parent', 'product', 'author')
        labels = {
            'star': '',
            'message': ''
        }
        widgets = {
            'message': forms.Textarea(
                attrs={'placeholder': 'comments', 'class': 'form-control w-100', 'id': 'contactcomment'})
        }
