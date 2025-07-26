from rest_framework import serializers
from markets.models import MarketProduct
from .models import Product, Category, Unit, Supplier


class ProductSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(
        max_length=50,
        required=True,
        error_messages={'required': 'Barkod boş qoyula bilməz!'}
    )
    name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'Ad boş qoyula bilməz!'}
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={'required': 'Alış qiyməti boş qoyula bilməz!'}
    )

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Kateqoriya boş qoyula bilməz!'}
    )
    unit = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Unit.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Vahid boş qoyula bilməz!'}
    )
    supplier = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Supplier.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Tədarükçü boş qoyula bilməz!'}
    )

    is_active = serializers.BooleanField(default=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['product_creator'] = user
        validated_data['update'] = True

        product = super().create(validated_data)

        MarketProduct.objects.create(
            market=user.market,
            product=product,
            quantity=validated_data.get('quantity', 0)
        )

        return product

    def update(self, instance, validated_data):
        validated_data['update'] = True
        return super().update(instance, validated_data)

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Kateqoriya adı boş qoyula bilməz!'}
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_by_center', 'created_at', 'updated_at']
        read_only_fields = ['created_by_center', 'created_at', 'updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'Tədarükçü adı boş qoyula bilməz!'}
    )
    phone = serializers.CharField(
        max_length=20,
        required=True,
        error_messages={'blank': 'Telefon nömrəsi boş ola bilər, amma daxil edilməlidir!'}
    )
    address = serializers.CharField(
        required=True,
        error_messages={'blank': 'Ünvan boş ola bilər, amma daxil edilməlidir!'}
    )
    is_active = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone', 'address', 'is_active','created_by_center', 'created_at','updated_at']
        read_only_fields = ['created_at','updated_at','created_by_center']

