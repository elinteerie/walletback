from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)  # Rating out of 5 stars
    completed_trades = models.IntegerField(default=0)  # Tracks number of completed trad

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    
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

class Trade(models.Model):
    CRYPTO_CHOICES = [
        ('spc', 'SPC'),
        ('tether', 'Tether'),
        ('btc', 'Bitcoin'),
        ('eth', 'Ethereum'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trades')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    crypto = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    min_buy = models.DecimalField(max_digits=10, decimal_places=2)
    max_buy = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    whatsapp_phone_number = models.CharField(max_length=50, null=True, blank=True)

    paypal_email = models.EmailField(null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    account_holder_name = models.CharField(max_length=100, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.whatsapp_phone_number:
            # Remove leading zero and add the country code based on user location
            if not self.whatsapp_phone_number.startswith('+'):
                self.whatsapp_phone_number = self.format_phone_number(self.whatsapp_phone_number, self.user.country)
        super().save(*args, **kwargs)

    def format_phone_number(self, phone_number, country):
        if phone_number.startswith('0'):
            # Remove leading zero
            phone_number = phone_number[1:]
        
        
        # Add appropriate country code based on the user's country
        country_code = ''
        if country == 'Nigeria':
            country_code = '+234'
        elif country == 'United States':
            country_code = '+1'
        # Add other country codes as needed

        return country_code + phone_number

    def __str__(self):
        return f'Trade by {self.user.email} - Crypto: {self.crypto}'
        



class TradeTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('payment_made', 'Payment_Made'),
    ]

    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_expiration = models.DateTimeField(default=timezone.now() + timedelta(minutes=20))

    def __str__(self):
        return f'Transaction by {self.buyer.email} for Trade ID: {self.trade.id}'

    def is_expired(self):
        return timezone.now() > self.transaction_expiration