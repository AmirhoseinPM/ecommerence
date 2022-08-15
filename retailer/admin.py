from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . import models


# Register your models here.

class RetailerAdmin(ModelAdmin):
    list_display = ('name', 'user', 'region', 'city', 'eco_num')
    search_fields = ('name', 'phone', 'eco_num')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    class Meta:
        ordering = ['user__date_joined']

admin.site.register(models.Retailer, RetailerAdmin)
