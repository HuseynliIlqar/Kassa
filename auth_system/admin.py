from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id','username', 'email', 'is_center', 'is_market', 'is_staff', 'is_superuser')
    list_filter = ('is_center', 'is_market', 'is_staff', 'is_superuser')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom fields', {'fields': (
            'is_center',
            'is_market',
            'is_stock_accses',
            'is_cash_desk_accses',
            'is_panel_accses',
            'created_by_center',
        )}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom fields', {'fields': (
            'is_center',
            'is_market',
            'is_stock_accses',
            'is_cash_desk_accses',
            'is_panel_accses',
            'created_by_center',
        )}),
    )
