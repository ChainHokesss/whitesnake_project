from django.db.models import Sum

from src.customers.models import CustomerModel, PurchaseHistory

class CustomerService:
    def get_customer(self, customer_id):
        return CustomerModel.objects.get(user = customer_id)

    def get_customer_cars(self, customer, car = None):
        filters = {
            'customer': customer
        }
        if car:
            filters['car'] = car

        return PurchaseHistory.objects.select_related('car').filter(**filters)

    def get_spend_money(self, customer):
        price = self.get_customer_cars(customer = customer).aggregate(Sum('price'))['price__sum']

        return price if price else 0

    def get_statistic(self, customer):
        data = {
            'spend money': self.get_spend_money(customer)
        }
        unique_purchase_history_set = self.get_customer_cars(customer = customer).distinct('car')
        customer_cars = {}

        for unique_purchase_history in unique_purchase_history_set:
            car = unique_purchase_history.car
            customer_cars[
                car.brand + " " + car.model
            ] = self.get_customer_cars(customer = customer, car = car).count()
        data['customer cars'] = customer_cars
        return data