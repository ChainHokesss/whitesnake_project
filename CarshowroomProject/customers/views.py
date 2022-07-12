from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, views, status, response

from .serializers import CustomerSerializer
from .models import CustomerModel
from carshowroom.tasks import accept_offer
from core.permissions import EmailConfirmPermission


class CreateOfferView(views.APIView):
    permission_classes = (IsAuthenticated, EmailConfirmPermission)

    def post(self, request):
        accept_offer.delay(request.user.id, request.data)
        return response.Response("Offer was created", status = status.HTTP_200_OK)


class CustomerViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    # permission_classes = [IsAdminUser]
    permission_classes = (AllowAny, )
    serializer_class = CustomerSerializer
    lookup_field = "user"
    queryset = CustomerModel.objects.all()