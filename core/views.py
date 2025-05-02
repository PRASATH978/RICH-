from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Product, UserProfile
from .forms import ProductForm


def home(request):
    return render(request, 'core/home.html')


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
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin account.")
    return render(request, 'core/admin_login.html')


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


@login_required
def user_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    today = timezone.now().date()
    products = Product.objects.filter(close_date__gte=today).order_by('-id')
    return render(request, 'core/dashboard.html', {
        'products': products,
        'user': request.user,
        'profile': profile
    })


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def user_details(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'core/user_details.html', {
        'user': request.user,
        'profile': profile
    })


def product_list(request):
    today = timezone.now().date()
    products = Product.objects.filter(close_date__gte=today).order_by('-id')
    return render(request, 'products/product_list.html', {'products': products})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('add_product')


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    products = Product.objects.all().order_by('-id')[:10]
    users = User.objects.all().order_by('-id')[:10]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'products': products,
        'users': users,
    }
    return render(request, 'admindashboard/base.html', context)


@user_passes_test(is_admin)
def admindashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    products = Product.objects.all().order_by('-id')[:10]
    users = User.objects.all().order_by('-id')[:10]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'products': products,
        'users': users,
    }
    return render(request, 'admindashboard/dashboard.html', context)


@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('add_product')
        else:
            messages.error(request, "Failed to add product. Please check the form.")
    else:
        form = ProductForm()

    products = Product.objects.all().order_by('-id')
    return render(request, 'products/add_product.html', {
        'form': form,
        'products': products
    })


def add_product_view(request):
    if request.method == 'POST':
        messages.success(request, 'Product added successfully!')
        return redirect('add_product')
    return render(request, 'your_template.html')



from django.contrib import messages

def some_view(request):
    try:
        # Some operation that could fail
        some_data = get_some_data()
    except Exception as e:
        messages.error(request, "Something went wrong: " + str(e))
        return redirect('error_page')
    return render(request, 'template.html', {'data': some_data})



from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product

def product_list(request):
    product_list = Product.objects.all()  # Or apply filters as needed
    paginator = Paginator(product_list, 6)  # Show 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/product_list.html', {'page_obj': page_obj})
