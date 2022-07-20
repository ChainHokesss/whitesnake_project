from django.db.models import Sum, Max

from src.carshowroom.models import CarshowroomModel, SupplierPurchaseHistory, CarshowroomCar
from src.customers.models import PurchaseHistory


class CarshowroomServices:
    def create_carshowroom(self, carshowroom_data):
        carshowroom, created = CarshowroomModel.objects.get_or_create(**carshowroom_data)
        return carshowroom

    def get_carshowroom(self, id):
        return CarshowroomModel.objects.prefetch_related('car_list').get(id=id)

    def get_purchase_history(self, carshowroom, car=None):
        filters = {
            'carshowroom':  carshowroom
        }
        if car:
            filters['car'] = car
        return PurchaseHistory.objects.filter(**filters)

    def get_carshowroom_car(self, carshowroom, car=None, price=None):
        filters = {
            'carshowroom': carshowroom
        }
        if car:
            filters['car'] = car
        if price:
            filters['price'] = price
        carshowroom_car = CarshowroomCar.objects.filter(**filters)
        return carshowroom_car

    def get_carshowroom_car_number(self, carshowroom, car):
        carshowroom_car_number = self.get_carshowroom_car(
            carshowroom=carshowroom, car=car
        ).aggregate(Sum('number'))['number__sum']
        return carshowroom_car_number if carshowroom_car_number else 0

    def get_carshowroom_income(self, carshowroom):
        income = self.get_purchase_history(carshowroom).aggregate(Sum('price'))['price__sum']
        return income if income else 0

    def get_amount_of_spend_money(self, carshowroom):
        total_amount = SupplierPurchaseHistory.objects.filter(
            carshowroom=carshowroom
        ).aggregate(Sum('total_amount'))['total_amount__sum']
        return total_amount if total_amount else 0

    def get_max_price(self, carshowroom):
        max_price = self.get_carshowroom_car(carshowroom=carshowroom).aggregate(Max('price'))['price__max']
        return max_price if max_price else 0

    def get_car_with_max_price(self, carshowroom):
        return self.get_carshowroom_car(carshowroom).order_by('-price').first()

    def get_statistics(self, carshowroom):
        data = {
            'income': self.get_carshowroom_income(carshowroom),
            'number of sold cars': self.get_purchase_history(carshowroom).count(),
            'amount of spend money': self.get_amount_of_spend_money(carshowroom)
        }
        cars = {}
        car_list = carshowroom.car_list.all()

        for car in car_list:
            cars[car.brand + car.model] = "number of cars "
            cars[car.brand + car.model] += str(self.get_carshowroom_car_number(carshowroom=carshowroom, car=car))
            cars[car.brand + car.model] += " number of sold cars "
            cars[car.brand + car.model] += str(self.get_purchase_history(carshowroom=carshowroom, car=car).count())

        data['carshowroom cars'] = cars
        carshowroom_car = self.get_car_with_max_price(carshowroom)
        if carshowroom_car:
            car_max_price = {
                'name': carshowroom_car.car.brand + carshowroom_car.car.model,
                'price': carshowroom_car.price
            }
            data['car with max price'] = car_max_price

        return data
