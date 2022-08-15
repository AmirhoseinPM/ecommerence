from django.urls import path
from . import views

urlpatterns =[
    # vendor main page
    path('', views.mainpage, name='vendor'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('edit_vendor/', views.edit_vendor, name='edit_vendor'),

    # show base products
    path('local_products/', views.local_products, name='local_products'),
    path('local_brands/<brand_slug>', views.brand_local_product, name='local_brands'),

   # creat vendor's product from base product
    path('add_product/<slug:product_slug>', views.add_product, name='add_product'),

    # add discount to a vendor's product
    path('add_discount/<slug:product_slug>', views.add_discount, name='add_discount'),

    # show discounted vendor's product
    path('discounts/', views.discounts, name='vendor_discounts'),

    # show vendor's products
    path('vendor_products/', views.vendor_products, name='vendor_products'),
    path('vendor_product/<slug:product_slug>', views.vendor_product, name='vendor_product'),
    path('vendor_brands/<brand_slug>', views.brand_view, name='vendor_brand'),
    path('vendor_sub_brands/<sub_brand_slug>', views.sub_brand_view, name='vendor_sub_brand'),

    # vendor product after non existing or date expired show as archive in base product
    path('local_product/<product_slug>', views.archives_product, name='archives_product'),


    path('search/', views.search, name='vendor_search'),

    # show retailers
    path('retailers/', views.retailers, name='vendor_retailers'),
    path('retailers/<retailer_slug>', views.retailer_view, name='retailer_view'),

    # orders
    path('order/current', views.current_order_view, name='vendor_current_orders'),
    path('order/sending', views.sending_order_view, name='vendor_sending_orders'),
    path('order/final', views.final_order_view, name='vendor_final_orders'),
    path('order/<order_id>', views.order_view, name='vendor_order_view'),

    # edit vendor's settlement conditions
    path('settlement', views.settlement, name='settlement'),

    # creat order
    path('vendor_cart/', views.vendor_cart, name='vendor_sell_cart'),
    path('order_success/', views.order_success, name='vendor_order_success')
]
