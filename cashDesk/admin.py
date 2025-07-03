from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "datetime", "total_price")
    search_fields = ("user__username",)
    list_filter = ("datetime",)
    inlines = [SaleItemInline]

admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)
