from django.contrib import admin
from . import models


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'created_at', 'paid_amount', 'total_number', 'seller_confirmation', 'buyer_confirmation', 'cash_settlement', 'draft_settlement', 'trust_settlement')
    search_fields = ('buyer__name', 'seller__name')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(models.Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'vendor_paid', 'price', 'quantity', 'discount_percent')
    search_fields = ('product__product__title',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(models.OrderItem, OrderItemAdmin)
