from django import forms
from .models import Cat


class CatCreateForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ('title', 'description', 'image')
