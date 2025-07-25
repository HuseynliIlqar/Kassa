from rest_framework import serializers
from markets.models import MarketProduct, MarketProductMovement


class MarketProductMovementSerializer(serializers.ModelSerializer):
    market_product = serializers.PrimaryKeyRelatedField(queryset=MarketProduct.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = MarketProductMovement
        fields = ['id', 'market_product', 'movement_type', 'quantity', 'user', 'created_at', 'comment']

    def validate(self, attrs):
        movement_type = attrs.get('movement_type')
        quantity = attrs.get('quantity')
        if movement_type not in ['in', 'out']:
            raise serializers.ValidationError("Invalid movement type.")
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        market_product = validated_data['market_product']
        movement_type = validated_data['movement_type']
        quantity = validated_data['quantity']

        if movement_type == 'out' and market_product.quantity < quantity:
            raise serializers.ValidationError("Insufficient stock for this product.")

        if movement_type == 'in':
            market_product.quantity += quantity
        elif movement_type == 'out':
            market_product.quantity -= quantity

        market_product.save()

        validated_data['user'] = user
        return super().create(validated_data)


class MarketProductSerializer(serializers.ModelSerializer):

    product = serializers.CharField(source='product.name')

    class Meta:
        model = MarketProduct
        fields = '__all__'
