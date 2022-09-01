from rest_framework.routers import SimpleRouter
from django.urls import path, include

from src.core.views import CarViewSet, UserViewSet, RestorePasswordView


user_router = SimpleRouter()
user_router.register(r'user', UserViewSet, basename='users')

cars_router = SimpleRouter()
cars_router.register(r'cars', CarViewSet, basename='cars')

core_urls = [
    path('api/', include(cars_router.urls)),
    path('api/', include(user_router.urls)),
    path('api/user/restore_password/<path:token>', RestorePasswordView.as_view())
]
