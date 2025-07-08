from rest_framework.permissions import BasePermission

class IsCenterUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_center
    
class IsAccsesStock(BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.is_authenticated and request.user.is_stock_accses

class IsAccsesPrice(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_price_accses