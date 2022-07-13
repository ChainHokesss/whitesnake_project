from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .yasg import urlpatterns as doc_urls
from config import settings
from src.carshowroom.urls import carshowroom_urls
from src.suppliers.urls import suppliers_urls
from src.core.urls import core_urls
from src.customers.urls import customers_urls

routers_urls = carshowroom_urls + suppliers_urls + core_urls + customers_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + routers_urls

urlpatterns += doc_urls

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns