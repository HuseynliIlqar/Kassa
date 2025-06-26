from django.contrib import admin
from .models import Market, MarketProduct


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'center')
    search_fields = ('name', 'center__username')

@admin.register(MarketProduct)
class MarketProductInline(admin.ModelAdmin):
    list_display = ('market', 'product', 'quantity')
    search_fields = ('market__name', 'product__name')
    list_filter = ('market', 'product')