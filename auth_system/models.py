from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_center = models.BooleanField(default=False)
    is_market = models.BooleanField(default=False)
    created_by_center = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='created_users')

    def __str__(self):
        return self.username


class RolePermission(models.Model):
    center = models.ForeignKey('auth_system.User', on_delete=models.CASCADE, related_name='permissions')
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code}"


class WorkerPermission(models.Model):
    center = models.ForeignKey('auth_system.User', on_delete=models.CASCADE)
    worker = models.ForeignKey('auth_system.User', on_delete=models.CASCADE, related_name='worker_permissions')
    permission = models.ForeignKey(RolePermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('worker', 'permission')
