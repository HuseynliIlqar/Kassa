from rest_framework import viewsets
from auth_system.permissions import IsCenterUser
from markets.models import MarketProduct
from .models import Product, Category, Supplier
from .serializers import ProductSerializer, CategorySerializer, SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsCenterUser]


    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            return self.queryset.filter(product_creator=center_user)
        return self.queryset.none()



    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        instance = self.get_object()
        instance.update = True
        instance.save()
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        instance.update = True
        instance.save()
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing product categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsCenterUser]

    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            return self.queryset.filter(created_by_center=center_user)
        return self.queryset.none()


    def perform_create(self, serializer):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            serializer.save(created_by_center=center_user)
        else:
            serializer.save(created_by_center=user)

    def perform_update(self, serializer):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            serializer.save(created_by_center=center_user)
        else:
            serializer.save(created_by_center=user)

    def perform_destroy(self, instance):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            instance.created_by_center = center_user
        else:
            instance.created_by_center = user
        instance.save()
        instance.delete()


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing suppliers.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsCenterUser]

    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            return self.queryset.filter(created_by_center=center_user)
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            serializer.save(created_by_center=center_user)
        else:
            serializer.save(created_by_center=user)

    def perform_update(self, serializer):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            serializer.save(created_by_center=center_user)
        else:
            serializer.save(created_by_center=user)

    def perform_destroy(self, instance):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            instance.created_by_center = center_user
        else:
            instance.created_by_center = user
        instance.save()
        instance.delete()