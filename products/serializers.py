from rest_framework import serializers
from .models import Product, Category, Unit, Supplier


class ProductSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(
        max_length=50,
        required=True,
        error_messages={'required': 'Barkod boş qoyula bilməz!'
})
    name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'Ad boş qoyula bilməz!'
})
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        error_messages={'required': 'Alış qiyməti boş qoyula bilməz!'
})
  # ForeignKey fields as SlugRelatedField
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Kateqoriya boş qoyula bilməz!'
})
    unit = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Unit.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Vahid boş qoyula bilməz!'
})
    supplier = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Supplier.objects.all(),
        required=True,
        allow_null=True,
        error_messages={'required': 'Tədarükçü boş qoyula bilməz!'
})

    #Read only fields
    is_active = serializers.BooleanField(default=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['product_creator'] = user
        return super().create(validated_data)

    class Meta:
        model = Product
        fields = '__all__'
