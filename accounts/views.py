from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm


def home(request):
    return render(request, 'home.html')

# Function to render the registration page and handle user registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # Save the user instance
            messages.success(request, "You have successfully registered! Please log in.")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'users/login.html', {'form': form})  # Render the form with errors
    form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})  # Render an empty form


# Function to render the login page and handle user login
def login_user(request):
    if request.method == "POST":
        identifier = request.POST['identifier']
        password = request.POST['password']
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')  # Render the login page



# Function to log out a user and redirect them to the login page
def logout_user(request):
    logout(request)
    return redirect('login')


# Function to render the password reset page and handle password reset
def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been successfully reset!')
            return redirect('login')  # Redirect to login after successful password reset
        else:
            messages.error(request, 'User not found.')
            return render(request, 'users/reset_password.html')
    return render(request, 'users/reset_password.html')


# Function to render the user deletion page and handle user deletion
@login_required
def delete_user(request):
    if request.method == 'POST':
        if request.user.username == request.POST.get('username'):
            request.user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('register')
        else:
            messages.error(request, 'Invalid username.')
    return render(request, 'users/delete_user.html')