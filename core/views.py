from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Product

from .models import UserProfile
def home(request):
    return render(request, 'core/home.html')

def user_login(request):
    # we'll add login logic later
    return render(request, 'core/login.html')

def admin_login(request):
    return render(request, 'core/admin_login.html')

@login_required
def user_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)  # Fetch user profile
    products = Product.objects.all()
    return render(request, 'core/dashboard.html', {
        'products': products,
        'user': request.user,
        'profile': profile  # 👈 This is what you're missing
    })



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
            return render(request, 'admin_dashboard/admin_dashboard.html')  # Redirect to Django admin
        else:
            messages.error(request, "Invalid credentials or not an admin account.")
    return render(request, 'core/admin_login.html')






from .models import UserProfile
from django.contrib.auth.models import User


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        state = request.POST.get("state")
        district = request.POST.get("district")
        photo = request.FILES.get("photo")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)

        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            mail=email,
            state=state,
            district=district,
            photo=photo
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'core/register.html')

from django.contrib.auth import logout

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def user_details(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'core/user_details.html', {
        'user': request.user,
        'profile': profile
    })







from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})
