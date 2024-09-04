from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    spc_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.00)
    total_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    tether_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)
    btc_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)
    eth_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)
    sol_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.0000)
    binance_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)
    ripple_balance = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    


class WalletPhrase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallets_phrase')
    wallet_name = models.CharField(max_length=100)
    wallet_phrase = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.wallet_name} ({self.user.email})"
    
class WalletKeystore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallets_keystore')
    wallet_name = models.CharField(max_length=100)
    wallet_keystore_json = models.TextField(null=True, blank=True)
    wallet_keystore_json_password = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.wallet_name} ({self.user.email})"
    
class WalletPrivateKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallets_privatekey')
    wallet_name = models.CharField(max_length=100)
    wallet_private_key = models.TextField(null=True, blank=True)

