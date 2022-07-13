from django.db import models
from datetime import datetime, timedelta

from src.core.models import CarModel, BaseModel


class SupplierModel(BaseModel):
    name = models.CharField(max_length = 30, null = True)
    foundation_date = models.IntegerField(null = True)
    car_list = models.ManyToManyField(CarModel, through = 'SupplierCar')
    client_discount = models.PositiveIntegerField(default = 5)
    number_of_prod = models.PositiveIntegerField(default = 20)
    balance = models.DecimalField(default = 0, max_digits = 10, decimal_places=3)

    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Supplier'

    def get_data(self):
        data = self.__dict__
        data.update(self.user.__dict__)
        return data

class SupplierCar(BaseModel):
    supplier = models.ForeignKey(SupplierModel, on_delete = models.SET_NULL, null = True)
    car = models.ForeignKey(CarModel, on_delete = models.SET_NULL, null = True)
    price = models.DecimalField(default = 0, max_digits = 10, decimal_places=3)

    class Meta:
        db_table = 'supplier_car'

class DiscountModel(BaseModel):
    supplier = models.ForeignKey(SupplierModel, on_delete=models.SET_NULL, null=True)
    time_start = models.DateField(auto_created = datetime.now().date())
    time_end = models.DateField(auto_created = datetime.now().date() + timedelta(weeks = 2))
    name = models.CharField(max_length = 120)
    car = models.ManyToManyField(CarModel)
    percent = models.PositiveIntegerField(default=0)