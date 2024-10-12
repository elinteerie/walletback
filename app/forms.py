from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, WalletPhrase, WalletKeystore, WalletPrivateKey
from .models import TradeTransaction

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


class TradeTransactionForm(forms.ModelForm):
    class Meta:
        model = TradeTransaction
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.trade = kwargs.pop('trade')
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < self.trade.min_buy:
            raise forms.ValidationError(f"The minimum buy is {self.trade.min_buy}. Please enter a higher amount.")
        if amount > self.trade.max_buy:
            raise forms.ValidationError(f"The maximum buy is {self.trade.max_buy}. Please enter a lower amount.")
        return amount