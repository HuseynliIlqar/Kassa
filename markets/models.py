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

    def __str__(self):
        return f"{self.product.name} in {self.market.name}"