from rest_framework import serializers

from src.core.models import CarModel
from src.core.services import CarsService, UsersService
from src.core.models import BaseUser

carsService = CarsService()
userseService = UsersService()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'body_type', 'issue_year', 'model', 'fuel_type', 'mileage')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return carsService.create_car(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return userseService.create_user(validated_data)

class RestorePasswordSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(max_length = 240)
    class Meta:
        model = BaseUser
        fields = ('password', 'password_2')