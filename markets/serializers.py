from rest_framework import serializers
from markets.models import MarketProduct, Market
from products.models import Product


class MarketProductSerializer(serializers.ModelSerializer):
    market = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)


    market_name = serializers.CharField(source='market.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = MarketProduct
        fields = ['id', 'market', 'market_name', 'product', 'product_name', 'quantity']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        center_user = getattr(user, 'created_by_center', None)
        if not center_user:
            raise serializers.ValidationError('İstifadəçinin created_by_center sahəsi boşdur.')
        market = Market.objects.filter(center=center_user).first()
        if not market:
            raise serializers.ValidationError('Bu istifadəçinin center-ə bağlı marketi tapılmadı.')
        validated_data['market'] = market
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('market', None)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        product = attrs.get('product')
        if not product:
            raise serializers.ValidationError('Məhsul seçilməyib.')
        if not hasattr(product, 'product_creator'):
            raise serializers.ValidationError('Məhsulun creator məlumatı tam deyil.')
        if user.created_by_center != product.product_creator:
            raise serializers.ValidationError('Yalnız product_creator-i öz created_by_center-in olan məhsulları stoka əlavə edə bilərsən.')
        return attrs
