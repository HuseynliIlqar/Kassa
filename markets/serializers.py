from rest_framework import serializers
from markets.models import MarketProduct

class MarketProductSerializer(serializers.ModelSerializer):
    market = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = MarketProduct
        fields = '__all__'
