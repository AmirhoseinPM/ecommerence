from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.mainpage, name='retailer'),
    path('edit_retailer/', views.edit_retailer, name='edit_retailer'),

    path('products/', views.products_view, name='products'),
    path('product/<product_slug>', views.product, name='product'),
    path('discount/', views.discounts, name='retailer_discounts'),

    path('vendors/', views.vendors_view, name='retailer_vendors'),
    path('vendors/<vendor_slug>', views.vendor, name='retailer_vendor'),

    path('cart/', views.carts, name='retailer_carts'),
    path('cart/<vendor_slug>', views.vendor_cart, name='vendor_cart'),
    path('cart/success/', views.order_success, name='order_success'),

    path('order/current', views.current_order_view, name='retailer_current_orders'),
    path('order/final', views.final_order_view, name='retailer_final_orders'),
]
