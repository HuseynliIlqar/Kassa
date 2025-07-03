from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('auth_system.urls')),
    path('products/', include('products.urls')),
    path('market/', include('markets.urls')),
    path('cashdesk/', include('cashDesk.urls')),

]
