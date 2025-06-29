from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketProductViewSet

router = DefaultRouter()
router.register(r'', MarketProductViewSet, basename='market-product')

urlpatterns = [
    path('', include(router.urls)),
]