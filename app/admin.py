from django.contrib import admin
from .models import CustomUser, Transaction, WalletPhrase, WalletKeystore, WalletPrivateKey


admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(WalletPhrase)
admin.site.register(WalletKeystore)
admin.site.register(WalletPrivateKey)
# Register your models here.
