from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    is_stock_accses = serializers.BooleanField(required=True)
    is_cash_desk_accses = serializers.BooleanField(required=True)
    is_panel_accses = serializers.BooleanField(required=True)
    is_price_accses = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = [ 'id','username',
                   'password',
                   'is_center',
                   'is_market',
                   'is_stock_accses',
                   'is_cash_desk_accses',
                   'is_panel_accses',
                   'is_price_accses'
        ]

        extra_kwargs = {
            'password': {'write_only': True},
            'is_center': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_center=False,
            is_market=True,
            is_stock_accses=validated_data['is_stock_accses'],
            is_cash_desk_accses=validated_data['is_cash_desk_accses'],
            is_panel_accses=validated_data['is_panel_accses'],
            is_price_accses=validated_data['is_price_accses'],
            created_by_center=self.context['request'].user
        )
        return user
