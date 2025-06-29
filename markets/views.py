from rest_framework import viewsets
from auth_system.permissions import IsCenterUser, IsStockAccessor
from .models import MarketProduct
from .serializers import MarketProductSerializer


class MarketProductViewSet(viewsets.ModelViewSet):
    queryset = MarketProduct.objects.all()
    serializer_class = MarketProductSerializer
    permission_classes = [IsStockAccessor]