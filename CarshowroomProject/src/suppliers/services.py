from django.db.models import Sum

from src.suppliers.models import SupplierModel
from src.carshowroom.models import SupplierPurchaseHistory

class SuppliersService:
    def get_supplier(self, supplier_id):
        return SupplierModel.objects.prefetch_related('car_list').get(id = supplier_id)

    def get_cars(self, supplier):
        return supplier.car_list.all()

    def get_sold_cars(self, **filters):
        return SupplierPurchaseHistory.objects.select_related('carshowroom').filter(**filters)

    def get_number_of_sold_cars(self, supplier, car = None, carshowroom = None):
        filters = {
            'supplier': supplier,
        }

        if car:
            filters['car'] = car
        if carshowroom:
            filters['carshowroom'] = carshowroom

        data = self.get_sold_cars(**filters).aggregate(Sum('number_of_purchases'))['number_of_purchases__sum']
        return data if data else 0

    def get_statistic(self, supplier):
        data = {
            'income': supplier.balance,
            'number_of_sold_cars ': self.get_number_of_sold_cars(supplier)
        }
        car_stats = {}
        car_list = self.get_cars(supplier)

        for car in car_list:
            car_stats[car.brand +" "+car.model] = self.get_number_of_sold_cars(supplier, car)

        data['car_stats'] = car_stats
        clients_stats = {}
        clients_purchases_set = self.get_sold_cars(supplier = supplier)

        for clients_purchases in clients_purchases_set:
            carshowroom = clients_purchases.carshowroom
            clients_stats[str(carshowroom.id) + " " +carshowroom.name] = self.get_number_of_sold_cars(
                supplier = supplier,
                carshowroom = carshowroom
            )

        data['number of clients bought cars'] = clients_stats
        return data