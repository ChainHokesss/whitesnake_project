import django_filters as filters

from src.core.models import CarModel, Brands, BodyTypes, FuelTypes


class CarFilter(filters.FilterSet):
    brand = filters.ChoiceFilter(choices=Brands.choices())
    body_type = filters.ChoiceFilter(choices=BodyTypes.choices())
    fuel_type = filters.ChoiceFilter(choices=FuelTypes.choices())
    issue_year = filters.NumberFilter(field_name='issue_year')
    issue_year__gt = filters.NumberFilter(field_name='issue_year', lookup_expr='gt')
    issue_year__lt = filters.NumberFilter(field_name='issue_year', lookup_expr='lt')
    mileage = filters.NumberFilter(field_name='issue_year')
    mileage__gt = filters.NumberFilter(field_name='mileage', lookup_expr='gt')
    mileage__lt = filters.NumberFilter(field_name='mileage', lookup_expr='lt')

    class Meta:
        model = CarModel
        fields = ['brand', 'body_type', 'fuel_type', 'issue_year', 'mileage']
