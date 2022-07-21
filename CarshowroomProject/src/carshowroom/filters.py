import django_filters as filters
from django_countries import countries

from src.carshowroom.models import CarshowroomModel


class CarshowroomFilter(filters.FilterSet):
    location = filters.ChoiceFilter(choices=countries)
    balance__gte = filters.NumberFilter(field_name='balance', lookup_expr='gte')
    balance__lte = filters.NumberFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = CarshowroomModel
        fields = ['location', 'balance']
