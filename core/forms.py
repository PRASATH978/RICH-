from django import forms
from django.contrib.auth.models import User
from .models import Product, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'open_date', 'close_date', 'nye_price', 'gain_price']
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'close_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'mail', 'state', 'district', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap class to all fields except for 'photo' (usually file inputs)
        for field_name, field in self.fields.items():
            if field_name != 'photo':
                field.widget.attrs['class'] = 'form-control'
