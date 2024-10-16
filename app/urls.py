# myapp/urls.py
from django.urls import path
from .views import (index, signin_view, signup_view, dashboard_view, custom_logout_view, send,
                    save_wallet_info, solindex, xrpindex, bnbindex, btcindex, ethindex, usdtindex,trade_transaction_success_view,
                    success_page, profile, kyc_view, stock, p2p, trade_detail_view, create_trade_transaction_view, cancel_transaction_view,mark_payment_made_view
                    
                    )



urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('dashboard/<int:user_id>/', dashboard_view, name='dashboard'),
    path('logout/', custom_logout_view, name='logout'),
    path('wallet/', save_wallet_info, name='save_wallet_info'),
    path('sol/', solindex, name='sol'),
    path('xrp/', xrpindex, name='xrp'),
    path('bnb/', bnbindex, name='bnb'),
    path('btc/', btcindex, name='btc'),
    path('eth/', ethindex, name='eth'),
    path('usdt/', usdtindex, name='usdt'),
    path('send/', send, name='send'),
    path('profile/', profile, name='user_profile'),
    path('kyc/', kyc_view, name='kyc'),  # Add the KYC view URL
    path('success', success_page, name='success_page'),
    path('stock/', stock, name='stock'),  # Add the KYC view URL
    path('p2p', trade_detail_view, name='p2p'),
    path('p2p/<int:trade_id>/buy/', create_trade_transaction_view, name='create_trade_transaction'),
    path('trade/success/<int:transaction_id>/', trade_transaction_success_view, name='trade_transaction_success'),
    path('trade/cancel/<int:transaction_id>/', cancel_transaction_view, name='cancel_transaction'),
    path('trade/mark_payment/<int:transaction_id>/', mark_payment_made_view, name='mark_payment_made'),


    
]
