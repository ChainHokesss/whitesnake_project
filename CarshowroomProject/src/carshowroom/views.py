from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import decorators, response
from django_filters import rest_framework as filters

from src.carshowroom.serializers import CarshowroomSerializer
from src.carshowroom.models import CarshowroomModel
from src.carshowroom.services import CarshowroomServices
from src.carshowroom.filters import CarshowroomFilter


class CarshowroomViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = CarshowroomModel.objects.all()
    serializer_class = CarshowroomSerializer
    permission_classes = (AllowAny, )
    service = CarshowroomServices()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarshowroomFilter

    @decorators.action(methods=['GET'], detail=True)
    def get_statistics(self, request, pk):
        carshowroom = self.service.get_carshowroom(pk)
        return response.Response(self.service.get_statistics(carshowroom))
