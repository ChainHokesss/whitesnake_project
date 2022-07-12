from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import decorators, response, views, status

from .serializers import CarshowroomSerializer
from .models import CarshowroomModel
from .tasks import buy_suppliers_cars, accept_offer


class CarshowroomViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = CarshowroomModel.objects.all()
    serializer_class = CarshowroomSerializer
    permission_classes =  [AllowAny]

    @decorators.action(methods = ['GET'], detail = False)
    def test_function(self, request):
        buy_suppliers_cars()
        return response.Response("sdf")
