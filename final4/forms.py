from .models import Product
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('content',)