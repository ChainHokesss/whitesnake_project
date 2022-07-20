from rest_framework.serializers import ModelSerializer

from src.customers.models import CustomerModel


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ('user', 'balance')
        read_only_fields = ('user', )
