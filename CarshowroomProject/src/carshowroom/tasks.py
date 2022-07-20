import decimal
from celery import shared_task
from datetime import datetime
from django.db.models import F, Max, Sum
from decimal import Decimal

from src.carshowroom.models import (
    CarshowroomModel,
    CarshowroomCar,
    SupplierPurchaseHistory,
    CarshowroomDiscountModel
)
from src.core.models import CarModel
from src.suppliers.models import SupplierCar
from src.suppliers.models import DiscountModel
from src.customers.models import PurchaseHistory, CustomerModel


def number_of_car_purchases(car, carshowroom):
    return PurchaseHistory.objects.filter(car=car, carshowroom=carshowroom, is_active=True).count()


def max_percent_discount(car, supplier=None, carshowroom=None):
    discount = None
    data = {
        'car': car,
        'time_start__lte': datetime.now(),
        'time_end__gte': datetime.now(),
        'is_active': True
    }

    if supplier and not carshowroom:
        data['supplier'] = supplier
        discount = DiscountModel.objects.filter(**data).aggregate(Max('percent'))['percent__max']
    if carshowroom and not supplier:
        data['carshowroom'] = carshowroom
        discount = CarshowroomDiscountModel.objects.filter(**data).aggregate(Max('percent'))['percent__max']

    return discount if discount else 0


def get_individual_discount(carshowroom, customer):
    number_of_purchases = PurchaseHistory.objects.filter(
        customer=customer,
        carshowroom=carshowroom,
        is_active=True
    ).count()

    if number_of_purchases >= carshowroom.number_of_prod:
        return carshowroom.client_discount

    return 0


def get_individual_supplier_discount(carshowroom, supplier):
    disc = SupplierPurchaseHistory.objects.filter(
        carshowroom=carshowroom, supplier=supplier, is_active=True
    ).aggregate(Sum('number_of_purchases'))['number_of_purchases__sum']
    return disc if disc else 0


@shared_task
def accept_supplier():
    carshowroom_set = CarshowroomModel.objects.all()
    for carshowroom in carshowroom_set:
        cars = CarModel.objects.filter(**carshowroom.car_characteristic, is_active=True)
        for car in cars:
            supplier_car = SupplierCar.objects.filter(car=car).order_by(
               (1 - max_percent_discount(supplier=F('supplier'), car=car) / 100) * F('price')
            ).first()
            if supplier_car:
                CarshowroomCar.objects.get_or_create(
                    price=supplier_car.price,
                    car=car,
                    carshowroom=carshowroom,
                    number=0,
                    supplier=supplier_car.supplier
                )


@shared_task
def buy_suppliers_cars():
    carshowroom_car_set = (
        CarshowroomCar.objects.select_related('supplier').select_related('carshowroom').select_related('car').all()
    )
    # сортировка сrashowroom_car_set по кол-ву купленных авто
    carshowroom_car_set = sorted(
        carshowroom_car_set,
        key=lambda x: number_of_car_purchases(x.car, x.carshowroom),
        reverse=True
    )
    for carshowroom_car in carshowroom_car_set:
        car = carshowroom_car.car
        supplier = carshowroom_car.supplier
        carshowroom = carshowroom_car.carshowroom

        supplier_car = SupplierCar.objects.filter(supplier=supplier, car=car, is_active=True).first()

        if supplier_car:
            individual_discount = get_individual_supplier_discount(carshowroom, supplier)
            discount_price = supplier_car.price * decimal.Decimal(
                (1 - (max_percent_discount(supplier=supplier, car=car) + individual_discount)/100)
            )
            if carshowroom.balance >= discount_price:
                carshowroom.balance -= Decimal(discount_price)
                supplier.balance += Decimal(discount_price)
                purchase_history, created = SupplierPurchaseHistory.objects.get_or_create(
                    car=car,
                    supplier=supplier,
                    carshowroom=carshowroom
                )
                purchase_history.number_of_purchases += 1
                purchase_history.total_amount += Decimal(discount_price)
                carshowroom_car.number += 1

                carshowroom.save()
                supplier.save()
                purchase_history.save()
                carshowroom_car.save()


@shared_task
def check_supplier_benefit():
    carshowroom_car_set = (
        CarshowroomCar.objects.select_related('supplier').select_related('carshowroom').select_related('car').all()
    )
    for carshowroom_car in carshowroom_car_set:
        car = carshowroom_car.car

        supplier_car = SupplierCar.objects.filter(car=car, is_active=True).order_by(
            (1 - max_percent_discount(supplier=F('supplier'), car=car) / 100) * F('price')
        ).first()

        if carshowroom_car.supplier != supplier_car.supplier:
            carshowroom_car.supplier = supplier_car.supplier
            carshowroom_car.save()


@shared_task
def accept_offer():
    customers_set = CustomerModel.objects.filter(user__email_is_confirmed=True)

    for customer in customers_set:
        car_set = CarModel.objects.filter(**customer.car_charact, is_active=True)
        carshowroom_car_set = CarshowroomCar.objects.filter(car__in=car_set, number__gt=0).order_by(
                (1 - max_percent_discount(carshowroom=F('carshowroom'), car=F('car'))/100 * F('price'))
        )

        if carshowroom_car_set.exists():
            carshowroom_car = carshowroom_car_set[0]
            carshowroom = carshowroom_car.carshowroom
            individual_discount = get_individual_discount(carshowroom=carshowroom, customer=customer)
            price = carshowroom_car.price * decimal.Decimal(
                (1 - (max_percent_discount(carshowroom=carshowroom, car=carshowroom_car.car) + individual_discount)/100)
            )

            if customer.balance >= price:
                customer.balance -= Decimal(price)
                carshowroom.balance += Decimal(price)
                carshowroom_car.number -= 1

                customer.save()
                carshowroom_car.save()
                carshowroom.save()

                PurchaseHistory.objects.create(
                    customer=customer,
                    car=carshowroom_car.car,
                    carshowroom=carshowroom,
                    price=price
                )
