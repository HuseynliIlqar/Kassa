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
        sales_qs = self.get_queryset().filter(user=user, datetime__date=today)
        total = sales_qs.aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
        serializer = self.get_serializer(sales_qs, many=True)
        kassir_center = getattr(user, 'created_by_center', None)
        kassir_center_id = kassir_center.id if kassir_center else None
        kassir_center_name = str(kassir_center) if kassir_center else None
        return Response({
            'date': str(today),
            'cashier_id': user.id,
            'cashier_username': user.username,
            'cashier_center_id': kassir_center_id,
            'cashier_center_name': kassir_center_name,
            'total_sales_count': sales_qs.count(),
            'total_sales_amount': total,
            'sales': serializer.data
        })

    @action(detail=False, methods=['post'], url_path='reset-sales')
    def reset_sales(self, request):
        user = request.user
        today = timezone.now().date()
        sales = Sale.objects.filter(user=user, datetime__date=today, is_counted=False)
        sales_count = sales.count()
        total = sales.aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
        serializer = self.get_serializer(sales, many=True)
        kassir_center = getattr(user, 'created_by_center', None)
        kassir_center_id = kassir_center.id if kassir_center else None
        kassir_center_name = str(kassir_center) if kassir_center else None
        # Satışları hesabatlanmış kimi işarələ
        sales.update(is_counted=True)
        return Response({
            'date': str(today),
            'cashier_id': user.id,
            'cashier_username': user.username,
            'cashier_center_id': kassir_center_id,
            'cashier_center_name': kassir_center_name,
            'total_sales_count': sales_count,
            'total_sales_amount': total,
            'sales': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='return-item')
    def return_item(self, request):
        sale_id = request.data.get('sale_id')
        sale_item_id = request.data.get('sale_item_id')
        return_quantity = int(request.data.get('return_quantity', 0))
        if not sale_id or not sale_item_id or return_quantity <= 0:
            return Response({'error': 'sale_id, sale_item_id və return_quantity göndərilməlidir.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sale_item = Sale.objects.get(id=sale_id).items.get(id=sale_item_id)
        except Sale.DoesNotExist:
            return Response({'error': 'Satış tapılmadı.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Satış məhsulu tapılmadı.'}, status=status.HTTP_404_NOT_FOUND)
        if sale_item.returned_quantity + return_quantity > sale_item.quantity:
            return Response({'error': 'Qaytarılacaq miqdar satış miqdarından çox ola bilməz.'}, status=status.HTTP_400_BAD_REQUEST)
        sale_item.returned_quantity += return_quantity
        sale_item.save()
        return Response({'message': 'Qaytarma uğurla qeydə alındı.', 'sale_item_id': sale_item.id, 'returned_quantity': sale_item.returned_quantity})

    @action(detail=False, methods=['get'], url_path='all-cashiers-day-summary')
    def all_cashiers_day_summary(self, request):
        today = timezone.now().date()
        sales_qs = self.get_queryset().filter(datetime__date=today)
        from collections import defaultdict
        cashier_data = defaultdict(lambda: {
            'cashier_id': None,
            'cashier_username': '',
            'cashier_center_id': None,
            'cashier_center_name': '',
            'total_sales_count': 0,
            'total_sales_amount': 0,
            'sales': []
        })
        for sale in sales_qs:
            user = sale.user
            kassir_center = getattr(user, 'created_by_center', None)
            kassir_center_id = kassir_center.id if kassir_center else None
            kassir_center_name = str(kassir_center) if kassir_center else None
            key = user.id
            cashier_data[key]['cashier_id'] = user.id
            cashier_data[key]['cashier_username'] = user.username
            cashier_data[key]['cashier_center_id'] = kassir_center_id
            cashier_data[key]['cashier_center_name'] = kassir_center_name
            cashier_data[key]['total_sales_count'] += 1
            cashier_data[key]['total_sales_amount'] += float(sale.total_price)
            cashier_data[key]['sales'].append(SaleSerializer(sale, context={'request': request}).data)
        return Response({
            'date': str(today),
            'cashiers': list(cashier_data.values())
        })

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        sale = self.get_object()
        if not sale.is_cart:
            return Response({'detail': 'Bu səbət artıq satışa çevrilib.'}, status=status.HTTP_400_BAD_REQUEST)
        # Stokdan çıx və satışa çevir
        total_price = 0
        user = sale.user
        center_user = getattr(user, 'created_by_center', None)
        market = None
        if center_user:
            from markets.models import MarketProduct, Market
            market = Market.objects.filter(center=center_user).first()
        for item in sale.items.all():
            product = item.product
            quantity = item.quantity
            price = product.price or 0
            if market:
                market_product = MarketProduct.objects.get(market=market, product=product)
                market_product.quantity -= quantity
                market_product.save()
            item.price = price
            item.save()
            total_price += price * quantity
        sale.total_price = total_price
        sale.is_cart = False
        sale.save()
        return Response({'detail': 'Səbət satışa çevrildi.', 'sale_id': sale.id})

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        user = request.user
        sale = Sale.objects.filter(user=user, is_cart=True).first()
        if not sale:
            return Response({'detail': 'Aktiv səbət tapılmadı.'}, status=status.HTTP_400_BAD_REQUEST)
        # Stokdan çıx və satışa çevir
        total_price = 0
        center_user = getattr(user, 'created_by_center', None)
        market = None
        if center_user:
            from markets.models import MarketProduct, Market
            market = Market.objects.filter(center=center_user).first()
        for item in sale.items.all():
            product = item.product
            quantity = item.quantity
            price = product.price or 0
            if market:
                market_product = MarketProduct.objects.get(market=market, product=product)
                market_product.quantity -= quantity
                market_product.save()
            item.price = price
            item.save()
            total_price += price * quantity
        sale.total_price = total_price
        sale.is_cart = False
        sale.save()
        return Response({'detail': 'Səbət satışa çevrildi.', 'sale_id': sale.id})

    # Günlük satışlar və statistikalar yalnız is_cart=False üçün hesablanır
    def get_queryset(self):
        qs = super().get_queryset()
        # Yalnız satışa çevrilmiş və is_counted=False olmayanları qaytar
        if self.action in ['list', 'day_summary', 'all_cahiers_day_summary']:
            return qs.filter(is_cart=False, is_counted=False)
        return qs
