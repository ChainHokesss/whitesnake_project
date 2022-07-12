from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins, permissions, decorators, generics

from core.serializers import CarSerializer, CarModel
from .models import SupplierModel
from .serializers import SupplierSerializer, SupplierCarSerializer, DiscountSerializer
from .services import SuppliersService


class SuppliersViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = SupplierSerializer
    queryset = SupplierModel.objects.all()
    permission_classes = [permissions.AllowAny]
    service = SuppliersService()

    @decorators.action(methods = ['GET'], detail = True)
    def get_cars(self, request, pk):
        cars = self.service.get_cars(supplier_id = pk)
        return Response(CarSerializer(cars, many = True).data)

class SupplierCarViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SupplierCarSerializer
    permission_classes = [permissions.AllowAny]

class SuppliersDiscountView(generics.CreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.AllowAny]




