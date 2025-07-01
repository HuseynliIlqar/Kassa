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
        created_markets = self.request.user.created_users.values_list('id', flat=True)
        return MarketProduct.objects.filter(market_id__in=created_markets)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not user.is_stock_accses:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().create(request, *args, **kwargs)
