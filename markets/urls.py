from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketProductListAPIView, StockSessionCreateAPIView, \
    StockSessionListWithItemsAPIView, StockSessionReceiptHTMLView

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('list/', MarketProductListAPIView.as_view(), name='market-product-list'),
    path('stock-sessions/', StockSessionListWithItemsAPIView.as_view(), name='stock-session-list'),
    path('stock-session/<int:pk>/receipt/', StockSessionReceiptHTMLView.as_view(), name='stock-receipt'),
    path('stock,',StockSessionListWithItemsAPIView.as_view(),name='stock-session-list'),


]

urlpatterns += [
    path("stock-bulk/", StockSessionCreateAPIView.as_view(), name="stock-bulk"),
]