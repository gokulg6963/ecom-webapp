
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, ProductForm
from .models import Product, Order
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_staff

def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    return render(request, 'shop/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
    return render(request, 'shop/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        qty = int(request.POST['quantity'])
        total = qty * product.price
        Order.objects.create(user=request.user, product=product, quantity=qty, total_price=total)
        return render(request, 'shop/order_summary.html', {
            'product': product,
            'quantity': qty,
            'total': total
        })
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'shop/add_product.html', {'form': form})


def register_admin(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            return redirect('login')
    return render(request, 'shop/register.html', {'form': form})
