from rest_framework import viewsets
from auth_system.permissions import IsCenterUser
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsCenterUser]
