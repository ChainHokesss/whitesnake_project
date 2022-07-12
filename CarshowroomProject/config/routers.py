from django.urls import path, include
from rest_framework.routers import SimpleRouter

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

routers_urls = [
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