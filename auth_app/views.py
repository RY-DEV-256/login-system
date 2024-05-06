from django.shortcuts import render,redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'auth_app/index.html')

@login_required
def home(request):
    username = request.user.get_username()
    return render(request, 'auth_app/home.html', {'username':username})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully")
            return redirect('login')
        else:
            messages.warning(request, 'Registration Failed!')
            return render(request, 'auth_app/register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'auth_app/register.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Login Failed! : Invalid username or password.')
                return render(request, 'auth_app/login.html', {'form':form})
    else:
        form = LoginForm()
        return render(request, 'auth_app/login.html', {'form':form})
    
def logout_view(request):
    logout(request)
    return redirect('login')