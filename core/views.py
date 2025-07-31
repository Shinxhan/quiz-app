from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category    
from .models import Quiz

def category_quizzes(request, category_id):
    quizzes = Quiz.objects.filter(category_id=category_id)
    return render(request, 'core/quizzes_by_category.html', {'quizzes': quizzes})

def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

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