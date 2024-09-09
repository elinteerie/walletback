from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, WalletPhrase, WalletKeystore, WalletPrivateKey

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)



class WalletPhraseForm(forms.ModelForm):
    class Meta:
        model = WalletPhrase
        fields = ['wallet_phrase']
        widgets = {
            'wallet_phrase': forms.Textarea(attrs={'rows': 3}),
        }

class WalletKeystoreForm(forms.ModelForm):
    class Meta:
        model = WalletKeystore
        fields = ['wallet_keystore_json', 'wallet_keystore_json_password']
        widgets = {
            'wallet_keystore_json': forms.Textarea(attrs={'rows': 3}),
        }

class WalletPrivateKeyForm(forms.ModelForm):
    class Meta:
        model = WalletPrivateKey
        fields = ['wallet_private_key']
        widgets = {
            'wallet_private_key': forms.Textarea(attrs={'rows': 3}),
        }



class KYCForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['address', 'postal_code', 'city', 'country']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
