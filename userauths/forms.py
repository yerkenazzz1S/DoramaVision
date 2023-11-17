from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'pattern': r'[A-Za-z0-9_-]{3,15}',
            'id': 'user_login',
            'class': 'input',
            'size': '20',
            'name': "user_login"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'pattern': r'[A-Za-z0-9_-]{3,15}',
            'id': 'user_email',
            'class': 'input',
            'size': '20',
            'name': "user_email"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            'id': 'pass1',
            'class': 'input',
            'size': '20',
            'name': "pass1"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            'id': 'pass2',
            'class': 'input',
            'size': '20',
            'name': "pass2"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']

