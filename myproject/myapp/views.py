from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import RegisterForm, ProductForm
from .models import Product, CartItem

from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def store(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@login_required
def admin_add_product(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')  # หรือ 'admin_dashboard'
    else:
        form = ProductForm()
    return render(request, 'myapp/admin_add_product.html', {'form': form})


def admin_dashboard(request):
    return render(request, 'myapp/admin_dashboard.html')

def get_product_count(request):
    product_count = Product.objects.count()
    return JsonResponse({'product_count': product_count})

def get_user_count(request):
    user_count = User.objects.count()
    return JsonResponse({'user_count': user_count})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.exclude(id=product_id).all()[:3]
    return render(request, 'myapp/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def admin_manage_product(request):
    if not request.user.is_staff:
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'admin_manage_product.html', {'products': products})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        product.delete()
        return redirect('admin_manage_product')
    return render(request, 'delete_product.html', {'product': product})

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return render(request, 'cart.html', {'message': 'Your cart is empty.'})
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        # ค้นหาสินค้าที่จะลบจากตะกร้า
        item = get_object_or_404(CartItem, id=product_id)
        item.delete()  # ลบสินค้าจากตะกร้า

        # หลังจากลบเสร็จ, redirect กลับไปยังหน้า cart หรือหน้าที่ต้องการ
        return redirect('cart')  # เปลี่ยนให้เหมาะสมกับ URL ของคุณ
    else:
        return redirect('cart')  # หรือหน้าที่ต้องการ
def checkout(request):
    # โค้ดสำหรับการเตรียมข้อมูลที่เกี่ยวกับการชำระเงิน
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout_view(request):
    if request.method == 'POST':
        # ทำการประมวลผลการชำระเงิน (เช่น การตัดยอด, การเชื่อมต่อกับระบบชำระเงิน)
        # จำลองการชำระเงินที่สำเร็จ
        success_checkout = True
        cart_items = []  # ข้อมูลสินค้าหลังจากชำระเงิน
        total_price = 0
        # ส่งค่าผลลัพธ์ให้กับ template
        return render(request, 'checkout.html', {'success_checkout': success_checkout, 'cart_items': cart_items, 'total_price': total_price})
    else:
        # ในกรณีที่เป็นการเข้าถึงครั้งแรก (GET) หรือไม่พบการ POST
        cart_items = []  # ข้อมูลสินค้าในตะกร้า
        total_price = 0
        return render(request, 'checkout.html', {'success_checkout': False, 'cart_items': cart_items, 'total_price': total_price})

        

        