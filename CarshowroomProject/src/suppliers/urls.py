from django.urls import path, include
from rest_framework.routers import SimpleRouter

from suppliers.views import SuppliersViewSet, SupplierCarViewSet, SuppliersDiscountView


suppliers_router = SimpleRouter()
suppliers_router.register(r'suppliers', SuppliersViewSet, basename='suppliers')

suppliers_car_router = SimpleRouter()
suppliers_car_router.register(r'cars', SupplierCarViewSet, basename='supplier_car')

suppliers_urls = [
    path('api/', include(suppliers_router.urls)),
    path('api/supplier/', include(suppliers_car_router.urls)),
    path('api/supplier/discount/', SuppliersDiscountView.as_view()),
]
