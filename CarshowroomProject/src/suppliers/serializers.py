from rest_framework import serializers
from django.shortcuts import get_object_or_404

from src.suppliers.models import SupplierModel, SupplierCar, DiscountModel
from src.core.models import CarModel


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierModel
        fields = ('name', 'foundation_date', 'car_list', 'client_discount', 'number_of_prod', 'balance')
        read_only_fields = ('id',)

class SupplierCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCar
        fields = '__all__'

class CarDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', )

class DiscountSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    time_start = serializers.DateField()
    time_end = serializers.DateField()
    name = serializers.CharField()
    percent = serializers.IntegerField()
    car = serializers.ListField(
        child = serializers.IntegerField(), write_only = True
    )

    def create(self, validated_data):
        discount = DiscountModel.objects.create(
            supplier = get_object_or_404(SupplierModel, id = validated_data.get('supplier_id')),
            time_start = validated_data.get('time_start'),
            time_end = validated_data.get('time_end'),
            name = validated_data.get('name'),
            percent = validated_data.get('percent')
        )
        for car_id in validated_data.get('car'):
            discount.car.add(CarModel.objects.get(id = car_id))

        return discount