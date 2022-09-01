from django.db import models

from src.core.models import BaseUser, CarModel, BaseModel
from src.carshowroom.models import CarshowroomModel


class CustomerModel(BaseModel):
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    purchase_history = models.ManyToManyField(CarshowroomModel, through='PurchaseHistory')
    car_charact = models.JSONField(default={})

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'


class PurchaseHistory(BaseModel):
    price = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    car = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'purchase_history'
