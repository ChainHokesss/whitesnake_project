from django.urls import path, include
from rest_framework.routers import SimpleRouter

from customers.views import CustomerViewSet, CreateOfferView

customers_router = SimpleRouter()
customers_router.register(r'customers', CustomerViewSet, basename='customer')

customers_urls = [
    path('api/customers/create_offer', CreateOfferView.as_view()),
    path('api/customers/', include(customers_router.urls)),
]