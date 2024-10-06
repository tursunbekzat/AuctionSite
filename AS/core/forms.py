# core/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'starting_price', 'image']
        
        # Опционально, вы можете добавить виджеты и классы CSS для стилей
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
