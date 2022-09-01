from django.db import models
from django_countries.fields import CountryField
from datetime import datetime, timedelta

from src.core.models import CarModel, BaseModel
from src.suppliers.models import SupplierModel


class CarshowroomModel(BaseModel):
    name = models.CharField(max_length=120)
    location = CountryField()
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    car_characteristic = models.JSONField()
    car_list = models.ManyToManyField(CarModel, through='CarshowroomCar')
    client_discount = models.PositiveIntegerField(default=5)
    number_of_prod = models.PositiveIntegerField(default=20)

    class Meta:
        db_table = 'carshowroom'


class CarshowroomCar(BaseModel):
    car = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.SET_NULL, null=True)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'carshowroom_car'


class SupplierPurchaseHistory(BaseModel):
    supplier = models.ForeignKey(SupplierModel, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    number_of_purchases = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'supplier_purchase_history'


class CarshowroomDiscountModel(BaseModel):
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete=models.SET_NULL, null=True)
    time_start = models.DateField(auto_created=datetime.now().date())
    time_end = models.DateField(auto_created=datetime.now().date() + timedelta(weeks=2))
    name = models.CharField(max_length=120)
    car = models.ManyToManyField(CarModel)
    percent = models.PositiveIntegerField(default=0)
