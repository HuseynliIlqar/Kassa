from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum

from auth_system import models
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], url_path='day-summary')
    def day_summary(self, request):
        user = request.user
        today = timezone.now().date()
        sales = Sale.objects.filter(user=user, datetime__date=today)
        total = sales.aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
        serializer = self.get_serializer(sales, many=True)
        kassir_center = getattr(user, 'created_by_center', None)
        kassir_center_id = kassir_center.id if kassir_center else None
        kassir_center_name = str(kassir_center) if kassir_center else None
        return Response({
            'date': str(today),
            'cashier_id': user.id,
            'cashier_username': user.username,
            'cashier_center_id': kassir_center_id,
            'cashier_center_name': kassir_center_name,
            'total_sales_count': sales.count(),
            'total_sales_amount': total,
            'sales': serializer.data
        })

    @action(detail=False, methods=['post'], url_path='reset-sales')
    def reset_sales(self, request):
        user = request.user
        today = timezone.now().date()
        sales = Sale.objects.filter(user=user, datetime__date=today)
        deleted_count = sales.count()
        sales.delete()
        return Response({
            'message': 'Bu günün bütün satışları silindi.',
            'deleted_sales_count': deleted_count
        }, status=status.HTTP_200_OK)
