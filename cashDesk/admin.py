from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    fields = ("id", "product", "quantity", "price", "returned_quantity")
    readonly_fields = ("id",)
    show_change_link = True


class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "datetime", "total_price")
    search_fields = ("user__username",)
    list_filter = ("datetime",)
    inlines = [SaleItemInline]


class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("id", "sale", "product", "quantity", "price", "returned_quantity")
    search_fields = ("sale__id", "product__name")
    list_filter = ("sale", "product")


admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
