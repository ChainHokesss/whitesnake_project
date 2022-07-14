from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import decorators, response, views, status

from src.carshowroom.serializers import CarshowroomSerializer
from src.carshowroom.models import CarshowroomModel
from src.carshowroom.services import CarshowroomServices
from src.carshowroom.tasks import buy_suppliers_cars, accept_offer


class CarshowroomViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = CarshowroomModel.objects.all()
    serializer_class = CarshowroomSerializer
    permission_classes =  (AllowAny, )
    service = CarshowroomServices()

    @decorators.action(methods=['GET'], detail=True)
    def carshowroom_statisctics(self, request, pk):
        carshowroom = self.service.get_carshowroom(pk)
        return response.Response(self.service.get_statistics(carshowroom))