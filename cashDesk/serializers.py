from rest_framework import serializers
from .models import Sale, SaleItem
from products.models import Product
from markets.models import MarketProduct, Market

class SaleItemSerializer(serializers.ModelSerializer):
    product_barcode = serializers.CharField(write_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_barcode', 'quantity']
        extra_kwargs = {'product': {'read_only': True}}

    def validate(self, attrs):
        barcode = attrs.pop('product_barcode', None)
        if barcode:
            try:
                product = Product.objects.get(barcode=barcode)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_barcode': 'Bu barkod ilə məhsul tapılmadı.'})
            attrs['product'] = product
        elif not attrs.get('product'):
            raise serializers.ValidationError({'product_barcode': 'Məhsul barkodu göndərilməlidir.'})
        return attrs

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    is_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'user', 'datetime', 'total_price', 'items', 'is_cart']
        read_only_fields = ['user', 'datetime', 'total_price']

    def validate(self, attrs):
        items = attrs.get('items', [])
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        center_user = getattr(user, 'created_by_center', None)
        if not center_user:
            raise serializers.ValidationError('İstifadəçinin created_by_center sahəsi boşdur.')
        market = Market.objects.filter(center=center_user).first()
        if not market:
            raise serializers.ValidationError('Bu istifadəçinin center-ə bağlı marketi tapılmadı.')
        for item in items:
            product = item.get('product')
            if not product:
                raise serializers.ValidationError('Məhsul tapılmadı və ya barkod yanlışdır.')
            if product.product_creator != center_user:
                raise serializers.ValidationError(f'{product.name} məhsulunu yalnız öz mərkəzinə aid məhsullar üçün satış edə bilərsən.')
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        center_user = getattr(user, 'created_by_center', None)
        market = Market.objects.filter(center=center_user).first()
        sale, created = Sale.objects.get_or_create(user=user, is_cart=True, defaults={'total_price': 0})
        total_price = sale.total_price or 0
        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            price = product.price or 0
            sale_item, item_created = SaleItem.objects.get_or_create(sale=sale, product=product, defaults={'quantity': quantity, 'price': price})
            if not item_created:
                sale_item.quantity += quantity
                sale_item.save()
            total_price += price * quantity
        sale.total_price = total_price
        sale.save()
        return sale
