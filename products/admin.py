from django.contrib import admin
from .models import Product, Supplier, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier', 'price', 'barcode', 'is_active')
    search_fields = ('name',)
    list_filter = ('supplier',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','created_by_center', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

