from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from auth_system.permissions import IsCenterUser, IsAccsesStock
from .models import MarketProduct
from .serializers import MarketProductSerializer


class MarketProductViewSet(viewsets.ModelViewSet):
    queryset = MarketProduct.objects.all()
    serializer_class = MarketProductSerializer
    permission_classes = [IsAccsesStock]

    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        return MarketProduct.objects.filter(market__center=center_user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not user.is_stock_accses:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().create(request, *args, **kwargs)
