from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'Settings/base.html')

def register(request):
    register_form = UserCreationForm()
    if request.method == "POST":
        register_form = UserCreationForm(request.POST)
    return render(request, 'Settings/register.html', {'register_form': register_form})

def login(request):
    login_form = AuthenticationForm()
    return render(request, 'Settings/login.html', {'login_form': login_form})
