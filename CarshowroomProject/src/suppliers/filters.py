import django_filters as filters

from src.suppliers.models import SupplierModel


class SupplierFilter(filters.FilterSet):
    foundation_date__gte = filters.NumberFilter(field_name='foundation_date', lookup_expr='gte')
    foundation_date__lte = filters.NumberFilter(field_name='foundation_date', lookup_expr='lte')
    balance__gte = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance__lte = filters.NumberFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = SupplierModel
        fields = ['foundation_date', 'balance']
