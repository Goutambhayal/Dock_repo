from django import forms
from django import forms

class StartTrading(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    TRADING_TYPE_CHOICES = [
                 # empty value works as a placeholder
        ('intraday', 'Intraday Trading(default)'),
        ('delivery', 'Delivery Trading'),
        ('options', 'Options Trading'),
        ('futures', 'Futures Trading'),
    ]

    trading_type = forms.ChoiceField(
        choices=TRADING_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

