from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, views, status, response

from src.customers.serializers import CustomerSerializer
from src.customers.models import CustomerModel
from src.customers.services import CustomerService
from src.core.permissions import EmailConfirmPermission


class CreateOfferView(views.APIView):
    permission_classes = (IsAuthenticated, EmailConfirmPermission)
    service = CustomerService()

    def post(self, request):
        customer = self.service.get_customer(request.user.id)
        customer.car_charact = request.data
        customer.save()
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