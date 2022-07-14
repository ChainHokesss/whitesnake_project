from rest_framework.routers import SimpleRouter
from django.urls import path, include

from src.carshowroom.views import CarshowroomViewSet

carshowroom_router = SimpleRouter()
carshowroom_router.register(r'carshowroom', CarshowroomViewSet, basename = 'carshowroom')


carshowroom_urls = [
    path('api/', include(carshowroom_router.urls)),
]