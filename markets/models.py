from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=100)
    center = models.OneToOneField('auth_system.User', on_delete=models.CASCADE, related_name='market')

    def __str__(self):
        return self.name

class MarketProduct(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='market_products')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        unique_together = ('market', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.market.name} ({self.quantity})"


class MarketProductMovement(models.Model):
    MOVEMENT_TYPES = (
        ("in", "Stock In"),         # Mal qəbulu
        ("out", "Stock Out"),       # Mal çıxışı (silinmə/zay)
    )
    market_product = models.ForeignKey(MarketProduct, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('auth_system.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    stock_session = models.ForeignKey(
        'markets.StockSession',  # və ya sadəcə 'StockSession' əgər eyni app-dadırsa
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movements'
    )


class StockSession(models.Model):
    center = models.ForeignKey('auth_system.User', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=[("in", "Stock In"), ("out", "Stock Out")])
    created_by = models.ForeignKey('auth_system.User', on_delete=models.SET_NULL, null=True, related_name='created_stock_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.movement_type.upper()} Session #{self.id} - {self.center.username}"
