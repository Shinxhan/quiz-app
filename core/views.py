from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'core/home.html')

def register(request):
 if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm_password']
 # Validate form
    if password != confirm:
        messages.error(request, "Passwords do not match.")
        return redirect('register')
    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists.")
        return redirect('register')
    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return redirect('register')
 # Save user
    User.objects.create(
    username=username,
    email=email,
    password=make_password(password)
    )
    messages.success(request, "Account created successfully. Please login.")
    return redirect('login')
 return render(request, 'core/register.html')