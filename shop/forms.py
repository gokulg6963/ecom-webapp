from django import forms    
from django.contrib.auth.models import User
from .models import Product

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
