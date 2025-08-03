from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
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

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "refresh token göndərilməyib."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Çıxış edildi."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Token artıq keçərsizdir və ya blacklisted edilib."}, status=status.HTTP_400_BAD_REQUEST)