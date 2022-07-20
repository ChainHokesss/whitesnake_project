from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import decorators, response

from src.carshowroom.serializers import CarshowroomSerializer
from src.carshowroom.models import CarshowroomModel
from src.carshowroom.services import CarshowroomServices


class CarshowroomViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = CarshowroomModel.objects.all()
    serializer_class = CarshowroomSerializer
    permission_classes = (AllowAny, )
    service = CarshowroomServices()

    @decorators.action(methods=['GET'], detail=True)
    def get_statistics(self, request, pk):
        carshowroom = self.service.get_carshowroom(pk)
        return response.Response(self.service.get_statistics(carshowroom))
