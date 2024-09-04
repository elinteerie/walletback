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
