from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def user_login(request):
    # we'll add login logic later
    return render(request, 'core/login.html')

def admin_login(request):
    return render(request, 'core/admin_login.html')

@login_required
def user_dashboard(request):
    return render(request, 'core/dashboard.html')



from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials or not a user account.")
    return render(request, 'core/login.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin/')  # Redirect to Django admin
        else:
            messages.error(request, "Invalid credentials or not an admin account.")
    return render(request, 'core/admin_login.html')




from .models import Product

@login_required
def user_dashboard(request):
    products = Product.objects.all()
    return render(request, 'core/dashboard.html', {'products': products})



from django.contrib.auth.models import User

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'core/register.html')


from django.contrib.auth import logout

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
