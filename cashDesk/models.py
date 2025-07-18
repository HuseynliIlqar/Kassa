from django.db import models
from auth_system.models import User
from products.models import Product

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_counted = models.BooleanField(default=False)
    is_cart = models.BooleanField(default=True)


    def __str__(self):
        return f"Sale #{self.id} by {self.user} on {self.datetime}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    returned_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Sale #{self.sale.id}"
