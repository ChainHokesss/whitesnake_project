from django.db import models

from core.models import BaseUser, CarModel
from carshowroom.models import CarshowroomModel


class CustomerModel(models.Model):
    balance = models.IntegerField(default = 0)
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key = True)
    purchase_history = models.ManyToManyField(CarshowroomModel, through = 'PurchaseHistory')

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'

    def get_data(self):
        data = self.__dict__
        data.update(self.user.__dict__)
        return data

class PurchaseHistory(models.Model):
    price = models.IntegerField(default = 0)
    car = models.ForeignKey(CarModel, on_delete = models.SET_NULL, null = True)
    carshowroom = models.ForeignKey(CarshowroomModel, on_delete = models.SET_NULL, null = True)
    customer = models.ForeignKey(CustomerModel, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'purchase_history'