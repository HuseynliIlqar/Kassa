from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_system.permissions import IsAccsesStock, IsCenterUser
from .models import MarketProduct, MarketProductMovement
from .serializers import MarketProductMovementSerializer, MarketProductSerializer


class MarketProductMovementViewSet(viewsets.ModelViewSet):
    queryset = MarketProductMovement
    serializer_class = MarketProductMovementSerializer
    permission_classes = [IsAccsesStock]

    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            return MarketProductMovement.objects.filter(market_product__market__center=center_user)
        return MarketProductMovement.objects.none()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCenterUser()]
        return super().get_permissions()



class MarketProductListAPIView(APIView):
    permission_classes = [IsAccsesStock]

    def get(self, request):
        user = request.user
        center_user = getattr(user, 'created_by_center', None)
        queryset = MarketProduct.objects.filter(market__center=center_user)
        serializer = MarketProductSerializer(queryset, many=True)
        return Response(serializer.data)
