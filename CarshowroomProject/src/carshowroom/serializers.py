from rest_framework import serializers

from src.carshowroom.models import CarshowroomModel


class CarshowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarshowroomModel
        fields = '__all__'
