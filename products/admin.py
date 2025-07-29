from django.contrib import admin
from .models import Product, Supplier, Unit, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'supplier', 'price', 'barcode', 'is_active')
    search_fields = ('name',)
    list_filter = ('unit', 'supplier')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','created_by_center', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

