from django.contrib import admin
from .models import CustomUser, Transaction, WalletPhrase, WalletKeystore, WalletPrivateKey, Trade, TradeTransaction


admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(WalletPhrase)
admin.site.register(WalletKeystore)
admin.site.register(WalletPrivateKey)
admin.site.register(Trade)
admin.site.register(TradeTransaction)

# Register your models here.
