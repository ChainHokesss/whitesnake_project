from rest_framework.serializers import ModelSerializer

from .models import CustomerModel


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ('user', 'balance')
        read_only_fields = ('user', )

