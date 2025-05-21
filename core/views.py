from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

# def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirect based on group
            if user.groups.filter(name='Gate Staff').exists():
                return redirect('gate:start_scanner')
            elif user.groups.filter(name='Meal Staff').exists():
                return redirect('meal:start_scanner')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'core/login.html')

def staff_logout(request):
    logout(request)
    return redirect('core:home')