from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Product, UserProfile
from .forms import ProductForm, UserForm, UserProfileForm
from django.db import IntegrityError


def home(request):
    return render(request, 'core/home.html')


# ---------- AUTH VIEWS ----------

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and not user.is_staff:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials or not a user account.")
    return render(request, 'core/login.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, "Invalid credentials or not an admin account.")
    return render(request, 'core/admin_login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


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

        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError:
            messages.error(request, "A user with that username or email already exists.")
            return redirect('register')

        # Get or create the profile in case the signal is not set up
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.full_name = full_name
        profile.phone = phone
        profile.mail = email
        profile.state = state
        profile.district = district
        if photo:
            profile.photo = photo
        profile.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'core/register.html')


# ---------- DASHBOARD ----------

@login_required
def user_dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    today = timezone.now().date()
    products = Product.objects.filter(close_date__gte=today).order_by('-id')
    return render(request, 'core/dashboard.html', {
        'products': products,
        'user': request.user,
        'profile': profile
    })


# ---------- PRODUCTS ----------

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/product_list.html', {'page_obj': page_obj})


@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('add_product')
    else:
        form = ProductForm()

    products = Product.objects.all().order_by('-id')
    return render(request, 'products/add_product.html', {
        'form': form,
        'products': products
    })


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('add_product')


# ---------- ADMIN DASHBOARD ----------

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    products = Product.objects.all().order_by('-id')[:10]
    users = User.objects.all().order_by('-id')[:10]
    return render(request, 'admindashboard/base.html', {
        'total_users': total_users,
        'total_products': total_products,
        'products': products,
        'users': users
    })


# ---------- USERS CRUD ----------

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'core/user_list.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('user_list')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'core/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_details')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'core/user_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_details')


# ---------- USER PROFILE VIEW ----------

@user_passes_test(lambda u: u.is_superuser)
def user_details(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'core/user_details.html', {'users': users})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Purchase  # Adjust based on your models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            payment_id = data.get("payment_id")

            if not request.user.is_authenticated:
                return JsonResponse({"status": "error", "error": "User not authenticated"}, status=403)

            product = Product.objects.get(id=product_id)

            # Save purchase record
            Purchase.objects.create(
                user=request.user,
                product=product,
                payment_id=payment_id
            )

            return JsonResponse({"status": "success"})

        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "error": "Invalid request method"}, status=405)



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Purchase  # Assuming a Purchase model exists

@login_required
def purchased_products(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('product')
    return render(request, 'core/purchased_products.html', {'purchases': purchases})
