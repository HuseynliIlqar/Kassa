from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_by_center = models.ForeignKey(
        'auth_system.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_categories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Unit(models.Model):
    """Vahidlər: ədəd, kq, litr və s."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by_center = models.ForeignKey(
        'auth_system.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_suppliers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    barcode = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=255,)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey('products.Supplier', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_creator = models.ForeignKey('auth_system.User', on_delete=models.SET_NULL, null=True, related_name='created_products')
    update = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.barcode})"

    def save(self, *args, **kwargs):
        if self.pk:
            old = Product.objects.get(pk=self.pk)
        super().save(*args, **kwargs)
