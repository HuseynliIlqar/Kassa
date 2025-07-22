from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from auth_system.permissions import IsCenterUser
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

    # @action(detail=False, methods=['get', 'post'], url_path='price-change-list', permission_classes=[IsAuthenticated])
    # def price_change_list(self, request):
    #     if request.method == 'GET':
    #         products = Product.objects.filter(update=True)
    #         data = [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in products]
    #         return Response(data)
    #     elif request.method == 'POST':
    #         products = Product.objects.filter(update=True)
    #         product_data = [
    #             {
    #                 'name': p.name,
    #                 'price': p.price,
    #                 'barcode': p.barcode,
    #             } for p in products
    #         ]
    #         html_content = render_to_string('price_change_list.html', {'products': product_data})
    #         for p in products:
    #             p.update = False
    #             p.save()
    #         return HttpResponse(html_content, content_type='text/html')

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


    # @action(detail=False, methods=['post'], url_path='get-prices-by-barcodes-html', permission_classes=[IsAuthenticated])
    # def get_prices_by_barcodes_html(self, request):
    #     """
    #     POST body: {"barcodes": ["1234567890", ...]}
    #     Returns: HTML with product info for given barcodes
    #     """
    #     barcodes = request.data.get('barcodes', [])
    #     if not isinstance(barcodes, list):
    #         return Response({'error': 'barcodes must be a list'}, status=400)
    #     products = Product.objects.filter(barcode__in=barcodes)
    #     product_data = [
    #         {
    #             'name': p.name,
    #             'price': p.price,
    #             'barcode': p.barcode,
    #         } for p in products
    #     ]
    #     html_content = render_to_string('price_change_list.html', {'products': product_data})
    #     return HttpResponse(html_content, content_type='text/html')


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