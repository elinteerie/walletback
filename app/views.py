# myapp/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, SignInForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import logout



def index(request):
    return render(request, 'app/index.html')



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard', args=[user.id]))
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
