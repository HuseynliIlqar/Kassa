from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_system.permissions import IsAccsesStock, IsCenterUser
from .models import MarketProduct, MarketProductMovement, StockSession
from .serializers import MarketProductMovementSerializer, MarketProductSerializer, BulkStockItemSerializer, \
    StockSessionSerializer, StockSessionWithItemsSerializer


class MarketProductMovementViewSet(viewsets.ModelViewSet):
    queryset = MarketProductMovement.objects.all()
    serializer_class = MarketProductMovementSerializer
    permission_classes = [IsCenterUser]

    def get_queryset(self):
        user = self.request.user
        center_user = getattr(user, 'created_by_center', None)
        if center_user:
            return MarketProductMovement.objects.filter(
                market_product__market__center=center_user,
                market_product__product__product_creator=center_user
            )
        return MarketProductMovement.objects.none()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCenterUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        market_product = serializer.validated_data['market_product']
        if market_product.product.product_creator != user.created_by_center:
            raise PermissionDenied("Bu məhsul sizin mərkəz tərəfindən yaradılmayıb.")
        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        market_product = serializer.validated_data.get(
            'market_product', serializer.instance.market_product
        )
        if market_product.product.product_creator != user.created_by_center:
            raise PermissionDenied("Bu məhsul sizin mərkəz tərəfindən yaradılmayıb.")
        serializer.save()

class MarketProductListAPIView(APIView):
    permission_classes = [IsAccsesStock]

    def get(self, request):
        user = request.user
        center_user = getattr(user, 'created_by_center', None)
        queryset = MarketProduct.objects.filter(
            market__center=center_user,
            product__product_creator=center_user
        )
        serializer = MarketProductSerializer(queryset, many=True)
        return Response(serializer.data)

class StockBulkMovementAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAccsesStock]

    def post(self, request):
        user = request.user
        center = user.created_by_center
        movement_type = request.data.get("movement_type")
        items = request.data.get("items", [])

        if movement_type not in ["in", "out"]:
            return Response({"detail": "movement_type must be 'in' or 'out'"}, status=400)

        serializer = BulkStockItemSerializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)

        created_ids = []

        for item in serializer.validated_data:
            barcode = item["product_barcode"]
            quantity = item["quantity"]

            try:
                market_product = MarketProduct.objects.select_related("product").get(
                    product__barcode=barcode,
                    market__center=center
                )
            except MarketProduct.DoesNotExist:
                return Response({"detail": f"Product with barcode {barcode} not found."}, status=404)

            # Məhsul mərkəzə aid olmalıdır
            if market_product.product.product_creator != center:
                return Response({"detail": f"Product {barcode} is not owned by your center."}, status=403)

            # 'out' zamanı stok kifayət etməlidir
            if movement_type == "out" and market_product.quantity < quantity:
                return Response({"detail": f"Insufficient stock for product {barcode}."}, status=400)

            # Stok dəyiş
            if movement_type == "in":
                market_product.quantity += quantity
            elif movement_type == "out":
                market_product.quantity -= quantity
            market_product.save()

            # Hərəkəti yadda saxla
            movement = MarketProductMovement.objects.create(
                market_product=market_product,
                movement_type=movement_type,
                quantity=quantity,
                user=user
            )
            created_ids.append(movement.id)

        return Response({
            "message": f"{movement_type.upper()} əməliyyatı tamamlandı.",
            "movement_ids": created_ids
        }, status=201)

class StockSessionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get (self, request):
        user = request.user
        center = user.created_by_center
        sessions = StockSession.objects.filter(center=center).prefetch_related('movements__market_product__product')
        serializer = StockSessionWithItemsSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data

        session_serializer = StockSessionSerializer(
            data={
                "movement_type": data.get("movement_type"),
                "comment": data.get("comment", "")
            },
            context={"request": request}
        )

        session_serializer.is_valid(raise_exception=True)
        stock_session = session_serializer.save(created_by=user)

        items = data.get("items", [])
        if not items:
            raise ValidationError("Ən azı bir məhsul əlavə olunmalıdır.")

        errors = []
        for item in items:
            item_serializer = BulkStockItemSerializer(data=item)
            item_serializer.is_valid(raise_exception=True)

            barcode = item_serializer.validated_data["product_barcode"]
            quantity = item_serializer.validated_data["quantity"]

            try:
                market_product = MarketProduct.objects.get(product__barcode=barcode)
            except MarketProduct.DoesNotExist:
                errors.append(f"Məhsul tapılmadı: {barcode}")
                continue

            if market_product.product.product_creator != user.created_by_center:
                errors.append(f"Məhsul sənin mərkəzinə aid deyil: {barcode}")
                continue

            if data["movement_type"] == "out" and market_product.quantity < quantity:
                errors.append(f"Kifayət qədər stok yoxdur: {barcode}")
                continue


            if data["movement_type"] == "in":
                market_product.quantity += quantity
            elif data["movement_type"] == "out":
                market_product.quantity -= quantity

            market_product.save()

            MarketProductMovement.objects.create(
                market_product=market_product,
                quantity=quantity,
                movement_type=data["movement_type"],
                stock_session=stock_session,
                user=user
            )

        if errors:
            return Response({
                "session_id": stock_session.id,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response({
            "session_id": stock_session.id,
            "message": "Stok sessiyası və məhsul hərəkətləri uğurla yaradıldı."
        }, status=status.HTTP_201_CREATED)

class StockSessionListWithItemsAPIView(ListAPIView):
    serializer_class = StockSessionWithItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        center = user.created_by_center
        return StockSession.objects.filter(center=center).prefetch_related('movements__market_product__product')

class StockSessionReceiptHTMLView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        session = get_object_or_404(StockSession, pk=pk, center=request.user.created_by_center)
        movements = MarketProductMovement.objects.filter(stock_session=session).select_related('market_product__product')

        return render(request, 'stock_receipt.html', {
            'session': session,
            'movements': movements
        })
