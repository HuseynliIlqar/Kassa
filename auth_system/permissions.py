from rest_framework.permissions import BasePermission
from auth_system.models import WorkerPermission


class IsCenterUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_center

class IsStockAccessor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        market_id = request.query_params.get('market_id')
        if not market_id:
            return False

        return WorkerPermission.objects.filter(
            worker=user,
            center__id=market_id,
            permission__code='can_access_stock'
        ).exists()