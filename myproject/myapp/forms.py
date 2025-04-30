from django import forms
from django.contrib.auth.models import User
import re
from .models import Product  # นำเข้า Product model

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your address'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords do not match")

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character")

        address = cleaned_data.get('address')
        if not address:
            raise forms.ValidationError("Address is required")

        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("Phone number is required")
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long")

        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
