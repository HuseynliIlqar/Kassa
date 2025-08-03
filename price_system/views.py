from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get', 'post'], url_path='price-change-list', permission_classes=[IsAuthenticated])
    def price_change_list(self, request):
        products = Product.objects.filter(update=True)

        # GET: Sadəcə update=True olan məhsulları göstər
        if request.method == 'GET':
            data = [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in products]
            return Response(data)

        # POST: Update=True olan məhsulları göstər və sonra update=False et
        elif request.method == 'POST':
            product_data = [
                {
                    'name': p.name,
                    'price': str(p.price),
                    'barcode': p.barcode,
                } for p in products
            ]

            # Məhsulları update=False et
            products.update(update=False)

            return Response({
                "message": "Yenilənmiş məhsullar qaytarıldı və update=false edildi.",
                "products": product_data
            })

    @action(detail=False, methods=['post'], url_path='get-prices-by-barcodes-html', permission_classes=[IsAuthenticated])
    def get_prices_by_barcodes_html(self, request):
        """
        POST body: {"barcodes": ["1234567890", ...]}
        Returns: JSON with product info for given barcodes
        """
        barcodes = request.data.get('barcodes', [])
        if not isinstance(barcodes, list):
            return Response({'error': 'barcodes must be a list'}, status=400)

        products = Product.objects.filter(barcode__in=barcodes)
        product_data = [
            {
                'name': p.name,
                'price': str(p.price),
                'barcode': p.barcode,
            } for p in products
        ]
        return Response({
            "message": "Sorğuya uyğun məhsullar",
            "products": product_data
        })
