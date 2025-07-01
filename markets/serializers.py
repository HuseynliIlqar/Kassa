from rest_framework import serializers
from markets.models import MarketProduct, Market
from products.models import Product


class MarketProductSerializer(serializers.ModelSerializer):
    market = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    market_name = serializers.CharField(source='market.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = MarketProduct
        fields = ['id', 'market', 'market_name', 'product', 'product_name', 'quantity']