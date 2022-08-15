from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . import models
# Register your models here.

class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'ordering', 'slug')
    search_fields = ('title', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class BrandAdmin(ModelAdmin):
    list_display = ('title', 'ordering', 'slug')
    search_fields = ('title', )
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProductAdmin(ModelAdmin):
    list_display = ('category', 'subcategory', 'brand', 'sub_brand', 'kg_retail_unit', 'packet_retail_unit','title', 'ordering', 'slug')
    search_fields = ('title', 'category', 'brand')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class SubCategoryAdmin(ModelAdmin):
    list_display = ('title', 'category', 'slug')
    search_fields = ('title',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class SubBrandAdmin(ModelAdmin):
    list_display = ('title', 'brand', 'slug')
    search_fields = ('title',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(models.SubBrand, SubBrandAdmin)

admin.site.register(models.SubCategory, SubCategoryAdmin)

admin.site.register(models.Product)

admin.site.register(models.Brand, BrandAdmin)

admin.site.register(models.Category, CategoryAdmin)


