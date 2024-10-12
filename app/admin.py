from django.contrib import admin
from .models import CustomUser, Transaction, WalletPhrase, WalletKeystore, WalletPrivateKey, Trade


admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(WalletPhrase)
admin.site.register(WalletKeystore)
admin.site.register(WalletPrivateKey)
admin.site.register(Trade)
# Register your models here.
