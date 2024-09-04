from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
