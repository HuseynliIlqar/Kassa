from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RolePermissionViewSet, WorkerPermissionViewSet, CreateUserView

router = DefaultRouter()
router.register(r'permissions', RolePermissionViewSet, basename='permission')
router.register(r'worker-permissions', WorkerPermissionViewSet, basename='worker-permission')

urlpatterns = router.urls

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
]

