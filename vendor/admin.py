from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . import models
# Register your models here.

class VendorAdmin(ModelAdmin):
    list_display = ('name', 'user', 'city', 'post_code')
    search_fields = ('name',)
    readonly_fields = ()

    filter_horizontal = ('cities', 'brands')
    list_filter = ()
    fieldsets = ()

    class Meta:
        ordering = ['user__date_joined']



class SettlementAdmin(ModelAdmin):
    list_display = ('get_vendor_name', 'cash', 'cash_discount_percent', 'draft', 'draft_days', 'trust', 'trust_days', 'date_added')
    search_fields = ()
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    class Meta:
        ordering = ['~date_added']

    def get_vendor_name(self, object):
        return object.vendor.name


class VendorProductAdmin(ModelAdmin):
    list_display = ('get_vendor_name', 'get_product_name', 'slug', 'date_added')
    search_fields = ()
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    class Meta:
        ordering = ['~date_added']

    def get_vendor_name(self, object):
        return object.vendor.name
    def get_product_name(self, object):
        return object.product.title

class DiscountAdmin(ModelAdmin):
    list_display = ('get_vendor_name', 'get_product_name', 'date_added', 'expire',
                    'step_one_number', 'step_one_percent', 'step_two_number', 'step_two_percent')
    search_fields = ()
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    class Meta:
        ordering = ['~date_added']


    def get_vendor_name(self, object):
        return object.vendor.name
    def get_product_name(self, object):
        return object.product.product.name


admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.VendorProduct, VendorProductAdmin)


admin.site.register(models.VendorSettlement, SettlementAdmin)
admin.site.register(models.Vendor, VendorAdmin)
