from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth_system.models import RolePermission, WorkerPermission, User
from auth_system.permissions import IsCenterUser
from auth_system.serializers import RolePermissionSerializer, WorkerPermissionSerializer, CreateUserSerializer


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated,IsCenterUser]

    def get_queryset(self):
        return RolePermission.objects.filter(center=self.request.user)

    def perform_create(self, serializer):
        serializer.save(center=self.request.user)

class WorkerPermissionViewSet(viewsets.ModelViewSet):
    queryset = WorkerPermission.objects.all()
    serializer_class = WorkerPermissionSerializer
    permission_classes = [IsAuthenticated, IsCenterUser]


    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(center=user)

class CreateUserView(APIView):
    permission_classes = [IsAuthenticated, IsCenterUser]

    def get(self, request, *args, **kwargs):
        workers = User.objects.filter(created_by_center=request.user)
        serializer = CreateUserSerializer(workers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data, context={'request': request})  # Pass request in context
        if serializer.is_valid():
            serializer.save(created_by_center=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
