from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class BodyTypes(Enum):
    SEDAN = 'sedan'
    COUPE = 'coupe'
    SPORT_CAR = 'sport car'
    STATION_VAGON = 'station vagon'
    HATCHBACK = 'hatchback'
    CONVERTIBLE = 'convertible'
    MINIVAN = 'minivan'
    PICKUP_TRACK = 'pickup truck'
    CROSSOVER = 'crossover'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class Brands(Enum):
    Audi = 'audi'
    Hyundai = 'Hyundai'
    Nissan = 'Nissan'
    Suzuki = 'Suzuki'
    BMW = 'BMW'
    Kia = 'Kia'
    Opel = 'Opel'
    Toyota = 'Toyota'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class FuelTypes(Enum):
    petrol = 'petrol'
    disel = 'disel'
    CNG = 'CNG'
    bio_disel = 'bio disel'
    electric = 'electric'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class BaseUser(AbstractUser):
    email_is_confirmed = models.BooleanField(default = False)

class CarModel(models.Model):
    id = models.AutoField(primary_key = True)
    brand = models.CharField(max_length = 30, choices = Brands.choices())
    body_type = models.CharField(max_length = 30, choices = BodyTypes.choices())
    issue_year = models.IntegerField()
    model = models.CharField(max_length = 40)
    fuel_type = models.CharField(default = FuelTypes.disel, max_length = 50, choices = FuelTypes.choices())
    mileage = models.IntegerField(default = 0)

    def get_data(self):
        return {
            'brand': self.brand,
            'body_type': self.body_type,
            'issue_year': self.issue_year,
            'model': self.model,
            'fuel_type': self.fuel_type,
            'mileage': self.mileage
        }

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        db_table = 'car'
