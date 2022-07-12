from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .yasg import urlpatterns as doc_urls
from config import settings
from core.views import CarViewSet, UserViewSet, RestorePasswordView
from suppliers.views import SuppliersViewSet, SupplierCarViewSet, SuppliersDiscountView
from carshowroom.views import CarshowroomViewSet
from customers.views import CustomerViewSet, CreateOfferView


cars_router = SimpleRouter()
cars_router.register(r'cars', CarViewSet, basename = 'cars')

suppliers_router = SimpleRouter()
suppliers_router.register(r'suppliers', SuppliersViewSet, basename = 'suppliers')

showroom_router = SimpleRouter()
showroom_router.register(r'autoservices', CarshowroomViewSet, basename = 'autoservices')

user_router = SimpleRouter()
user_router.register(r'user', UserViewSet, basename = 'users')

suppliers_car_router = SimpleRouter()
suppliers_car_router.register(r'cars', SupplierCarViewSet, basename = 'supplier_car')

customers_router = SimpleRouter()
customers_router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(cars_router.urls)),
    path('api/', include(user_router.urls)),
    path('api/', include(suppliers_router.urls)),
    path('api/', include(showroom_router.urls)),
    path('api/supplier/', include(suppliers_car_router.urls)),
    path('api/supplier/discount/', SuppliersDiscountView.as_view()),
    path('api/customers/create_offer', CreateOfferView.as_view()),
    path('api/customers/', include(customers_router.urls)),
    path('api/user/restore_password/<path:token>', RestorePasswordView.as_view())
]

urlpatterns += doc_urls

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns