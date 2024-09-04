# myapp/urls.py
from django.urls import path
from .views import (index, signin_view, signup_view, dashboard_view, custom_logout_view, 
                    save_wallet_info,
                    )



urlpatterns = [
    path('', index, name='index'),
     path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('dashboard/<int:user_id>/', dashboard_view, name='dashboard'),
    path('logout/', custom_logout_view, name='logout'),
    path('wallet/', save_wallet_info, name='save_wallet_info'),
    
]
