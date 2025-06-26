from rest_framework import serializers
from .models import RolePermission, WorkerPermission, User


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'code', 'name']


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class WorkerPermissionSerializer(serializers.ModelSerializer):
    worker = UserShortSerializer(read_only=True)
    worker_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='worker')
    permission = RolePermissionSerializer(read_only=True)
    permission_id = serializers.PrimaryKeyRelatedField(queryset=RolePermission.objects.all(), write_only=True, source='permission')

    class Meta:
        model = WorkerPermission
        fields = '__all__'
        read_only_fields = ['center']

    def create(self, validated_data):
        validated_data['center'] = self.context['request'].user
        return super().create(validated_data)

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_center', 'is_market', 'id']
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
            created_by_center=self.context['request'].user
        )
        return user
