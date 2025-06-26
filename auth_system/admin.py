from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RolePermission, WorkerPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_center', 'is_market', 'is_staff', 'is_superuser')
    list_filter = ('is_center', 'is_market', 'is_staff', 'is_superuser')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('is_center', 'is_market','created_by_center')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom fields', {'fields': ('is_center', 'is_market', 'created_by_center')}),
    )

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'center')
    search_fields = ('code', 'name')
    list_filter = ('center',)

@admin.register(WorkerPermission)
class WorkerPermissionAdmin(admin.ModelAdmin):
    list_display = ('worker', 'permission')
    search_fields = ('worker__username', 'permission__code')
    list_filter = ('worker', 'permission')