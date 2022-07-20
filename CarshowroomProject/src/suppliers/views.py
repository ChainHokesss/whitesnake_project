from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins, permissions, decorators, generics, status

from src.core.serializers import CarSerializer
from src.suppliers.models import SupplierModel
from src.suppliers.serializers import SupplierSerializer, SupplierCarSerializer, DiscountSerializer
from src.suppliers.services import SuppliersService


class SuppliersViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = SupplierSerializer
    queryset = SupplierModel.objects.all()
    permission_classes = (permissions.AllowAny, )
    service = SuppliersService()

    @decorators.action(methods=('GET', ), detail=True)
    def get_cars(self, request, pk):
        cars = self.service.get_cars(supplier=self.service.get_supplier(pk))
        return Response(CarSerializer(cars, many=True).data)

    @decorators.action(methods=('GET', ), detail=True)
    def get_statistics(self, request, pk):
        supplier = self.service.get_supplier(supplier_id=pk)
        return Response(self.service.get_statistic(supplier), status=status.HTTP_200_OK)


class SupplierCarViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SupplierCarSerializer
    permission_classes = (permissions.AllowAny, )


class SuppliersDiscountView(generics.CreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = (permissions.AllowAny, )
