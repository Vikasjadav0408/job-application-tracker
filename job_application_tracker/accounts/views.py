from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from job_tracker.models import Application

@login_required
def dashboard_view(request):
    applications = Application.objects.filter(user=request.user)
    total_apps = applications.count()

    context = {
        'total_apps': total_apps,
        'applied': applications.filter(status='applied'),
        'interviewed': applications.filter(status='interview'),
        'offered': applications.filter(status='offer'),
        'rejected': applications.filter(status='rejected'),
    }
    return render(request, 'dashboard.html', context)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']  # ✅ collect email
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)  # ✅ save email
        login(request, user)
        return redirect('dashboard')  # ✅ go to dashboard after register

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
