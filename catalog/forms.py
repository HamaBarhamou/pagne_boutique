from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "name", "slug", "price", "thumbnail", "is_active"]
        widgets = {
            "category": forms.Select(attrs={"class": "inp"}),
            "name": forms.TextInput(attrs={"class": "inp"}),
            "slug": forms.TextInput(attrs={"class": "inp"}),
            "price": forms.NumberInput(attrs={"class": "inp", "min": 0}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "inp"}),
            "is_active": forms.CheckboxInput(attrs={"class": "chk"}),
        }
