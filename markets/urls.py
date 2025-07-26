from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketProductListAPIView, MarketProductMovementViewSet, StockSessionCreateAPIView, \
    StockSessionListWithItemsAPIView, StockSessionReceiptHTMLView

router = DefaultRouter()
router.register(r'stock', MarketProductMovementViewSet, basename='market-product')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', MarketProductListAPIView.as_view(), name='market-product-list'),
    path('stock-sessions/', StockSessionListWithItemsAPIView.as_view(), name='stock-session-list'),
    path('stock-session/<int:pk>/receipt/', StockSessionReceiptHTMLView.as_view(), name='stock-receipt'),


]

urlpatterns += [
    path("stock-bulk/", StockSessionCreateAPIView.as_view(), name="stock-bulk"),
]