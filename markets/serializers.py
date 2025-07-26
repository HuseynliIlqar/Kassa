from rest_framework import serializers
from markets.models import MarketProduct, MarketProductMovement, StockSession


class BulkStockItemSerializer(serializers.Serializer):
    product_barcode = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)


class MarketProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = MarketProduct
        fields = ['id', 'product', 'quantity', 'market']


class StockSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockSession
        fields = ['id', 'movement_type', 'created_at', 'comment']
        read_only_fields = ['id', 'created_at', 'center']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['center'] = user.created_by_center
        validated_data['created_by'] = user
        return super().create(validated_data)


class MarketProductMovementSerializer(serializers.ModelSerializer):
    market_product = MarketProductSerializer(read_only=True)
    market_product_id = serializers.PrimaryKeyRelatedField(
        source='market_product',
        queryset=MarketProduct.objects.all(),
        write_only=True
    )

    stock_session = StockSessionSerializer(read_only=True)
    stock_session_id = serializers.PrimaryKeyRelatedField(
        source='stock_session',
        queryset=StockSession.objects.all(),
        write_only=True,
        required=False
    )

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = MarketProductMovement
        fields = [
            'id',
            'market_product', 'market_product_id',
            'stock_session', 'stock_session_id',
            'movement_type',
            'quantity',
            'user',
            'created_at',
            'comment'
        ]

    def validate(self, attrs):
        movement_type = attrs.get('movement_type')
        quantity = attrs.get('quantity')

        if movement_type not in ['in', 'out']:
            raise serializers.ValidationError("Invalid movement type.")
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        market_product = validated_data['market_product']
        movement_type = validated_data['movement_type']
        quantity = validated_data['quantity']

        # Əgər stock_session ötürülməyibsə, avtomatik yaradılır
        stock_session = validated_data.get('stock_session')
        if not stock_session:
            stock_session = StockSession.objects.create(
                center=user.created_by_center,
                movement_type=movement_type,
                created_by=user,
                comment=validated_data.get('comment', '')
            )
            validated_data['stock_session'] = stock_session

        # Stok miqdarını dəyiş
        if movement_type == 'out' and market_product.quantity < quantity:
            raise serializers.ValidationError("Insufficient stock for this product.")

        if movement_type == 'in':
            market_product.quantity += quantity
        elif movement_type == 'out':
            market_product.quantity -= quantity

        market_product.save()

        validated_data['user'] = user
        return super().create(validated_data)


class MovementItemNestedSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='market_product.product.name')

    class Meta:
        model = MarketProductMovement
        fields = ['product', 'quantity']


class StockSessionWithItemsSerializer(serializers.ModelSerializer):
    items = MovementItemNestedSerializer(source='movements', many=True)

    class Meta:
        model = StockSession
        fields = ['id', 'movement_type', 'created_at', 'comment', 'items']
