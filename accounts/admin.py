from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

from accounts.models import Account, City, Region


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_vendor', 'is_retailer', 'phone')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CityAdmin(ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class RegionAdmin(ModelAdmin):
    list_display = ('code', 'name', 'city')
    search_fields = ('name', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
