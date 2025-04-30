from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('store/', views.store, name='store'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add_product/', views.admin_add_product, name='admin_add_product'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('get-product-count/', views.get_product_count, name='get_product_count'),
    path('get-user-count/', views.get_user_count, name='get_user_count'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/', views.product_list, name='product_list'),
    path('admin_manage_product/', views.admin_manage_product, name='admin_manage_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),  # แก้ไขเป็น cart_view แทน view_cart
path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

       path('checkout/', views.checkout, name='checkout'),  # เพิ่ม URL สำหรับ Checkout
]
