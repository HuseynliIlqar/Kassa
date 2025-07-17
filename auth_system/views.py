from rest_framework import viewsets
from auth_system.models import User
from auth_system.permissions import IsCenterUser
from auth_system.serializers import CreateUserSerializer

class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [IsCenterUser]

    def get_queryset(self):
        return User.objects.filter(created_by_center=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by_center=self.request.user)
