<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins, permissions, decorators, generics, status

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

    @decorators.action(methods = ['GET'], detail = True)
    def get_statistic(self, request, pk):
        supplier = self.service.get_supplier(supplier_id = pk)
        return Response(self.service.get_statistic(supplier), status = status.HTTP_200_OK)


class SupplierCarViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SupplierCarSerializer
    permission_classes = [permissions.AllowAny]

class SuppliersDiscountView(generics.CreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.AllowAny]
>>>>>>> Stashed changes
