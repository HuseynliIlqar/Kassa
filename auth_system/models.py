from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_center = models.BooleanField(default=False)
    is_market = models.BooleanField(default=False)
    is_stock_accses = models.BooleanField(default=False)
    is_cash_desk_accses = models.BooleanField(default=False)
    is_panel_accses = models.BooleanField(default=False)
    is_price_accses = models.BooleanField(default=False)
    created_by_center = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='created_users')

    def __str__(self):
        return self.username