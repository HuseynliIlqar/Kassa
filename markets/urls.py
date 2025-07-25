from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketProductListAPIView, MarketProductMovementViewSet

router = DefaultRouter()
router.register(r'stock', MarketProductMovementViewSet, basename='market-product')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', MarketProductListAPIView.as_view(), name='market-product-list'),
]