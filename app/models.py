from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
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



class Transaction(models.Model):
    CURRENCY_CHOICES = [
        ('SPC', 'SPC'),
        ('Tether', 'Tether'),
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('SOL', 'Solana'),
        ('Binance', 'Binance Coin'),
        ('Ripple', 'Ripple'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('inflow', 'Inflow'),
        ('outflow', 'Outflow'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    currency_type = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    timestamp = models.DateTimeField(auto_now_add=True)
    #success = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.user.email} - {self.currency_type} - {self.transaction_type} - {self.amount}"
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the transaction first
        #self.success = True
        self.update_user_balance()

    def update_user_balance(self):
        if self.currency_type == 'SPC':
            field_name = 'spc_balance'
        elif self.currency_type == 'Tether':
            field_name = 'tether_balance'
        elif self.currency_type == 'BTC':
            field_name = 'btc_balance'
        elif self.currency_type == 'ETH':
            field_name = 'eth_balance'
        elif self.currency_type == 'SOL':
            field_name = 'sol_balance'
        elif self.currency_type == 'Binance':
            field_name = 'binance_balance'
        elif self.currency_type == 'Ripple':
            field_name = 'ripple_balance'
        else:
            return  # No action for unsupported currencies

        if self.transaction_type == 'inflow':
            setattr(self.user, field_name, F(field_name) + self.amount)  # Increment balance
        elif self.transaction_type == 'outflow':
            setattr(self.user, field_name, F(field_name) - self.amount)  # Decrement balance
            

        
        
        
        # Save the updated balance to the user
        

