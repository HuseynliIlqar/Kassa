from django.contrib import admin
from .models import Market, MarketProduct, MarketProductMovement, StockSession


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'center')
    search_fields = ('name', 'center__username')

@admin.register(MarketProduct)
class MarketProductInline(admin.ModelAdmin):
    list_display = ('id','market', 'product', 'quantity')
    search_fields = ('market__name', 'product__name')
    list_filter = ('market', 'product')


@admin.register(MarketProductMovement)
class MarketProductMovementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'market_product',
        'movement_type',
        'quantity',
        'user',
        'created_at',
        'comment',
    )
    list_filter = (
        'movement_type',
        'created_at',
        'user',
        'market_product__market',
        'market_product__product',
    )
    search_fields = (
        'market_product__product__name',
        'market_product__market__name',
        'comment',
        'user__username',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


    def market(self, obj):
        return obj.market_product.market.name

    def product(self, obj):
        return obj.market_product.product.name

    market.short_description = "Market"
    product.short_description = "Product"


@admin.register(StockSession)
class StockSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'movement_type', 'center', 'created_by', 'created_at', 'short_comment')
    list_filter = ('movement_type', 'center', 'created_at')
    search_fields = ('center__username', 'created_by__username', 'comment')
    readonly_fields = ('created_at',)

    def short_comment(self, obj):
        return obj.comment[:30] + "..." if obj.comment and len(obj.comment) > 30 else obj.comment
    short_comment.short_description = 'Comment'
