from django.core.management.base import BaseCommand
from django.db.models import Min, Max
from datetime import datetime, timedelta
import random
import string
from django_countries import countries
from enum import Enum

from src.core.models import CarModel, BodyTypes, Brands, FuelTypes
from src.suppliers.models import SupplierModel, SupplierCar, DiscountModel
from src.carshowroom.models import CarshowroomModel, CarshowroomDiscountModel
from src.carshowroom.tasks import accept_supplier


class DefaultCharacteristics(Enum):
    body_type = random.choice(list(BodyTypes)).value
    fuel_type = random.choice(list(FuelTypes)).value
    issue_year__gte = random.randint(1990, datetime.now().year)
    issue_year__lte = random.randint(1990, datetime.now().year)
    mileage__gte = random.randint(0, 100000)
    mileage__lte = random.randint(0, 100000)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._generate_cars()
        self._generate_suppliers()
        self._generate_supplier_car()
        self._generate_carshowrooms()
        self._generate_suppliers_discounts()
        self._generate_carshowroom_discounts()
        accept_supplier.delay()

    def _generate_cars(self):
        for i in range(10):
            CarModel.objects.get_or_create(
                brand=random.choice(list(Brands)).value,
                body_type=random.choice(list(BodyTypes)).value,
                fuel_type=random.choice(list(FuelTypes)).value,
                issue_year=random.randint(1990, datetime.now().year),
                model=self.generate_random_string(random.randint(1, 4)),
                mileage=random.randint(0, 100000),
            )

    def _generate_suppliers(self):
        for i in range(10):
            SupplierModel.objects.get_or_create(
                name=self.generate_random_string(random.randint(4, 10)),
                foundation_date=random.randint(1900, datetime.now().year),
                client_discount=random.randint(0, 10),
                number_of_prod=random.randint(20, 500),
            )

    def _generate_supplier_car(self):
        for i in range(40):
            supplier_car, created = SupplierCar.objects.get_or_create(
                supplier=SupplierModel.objects.get(id=random.randint(
                    SupplierModel.objects.aggregate(Min('id'))['id__min'],
                    SupplierModel.objects.aggregate(Max('id'))['id__max']
                )),
                car=CarModel.objects.get(id=random.randint(
                    CarModel.objects.aggregate(Min('id'))['id__min'],
                    CarModel.objects.aggregate(Max('id'))['id__max']
                )),
            )
            supplier_car.price = random.randint(5000, 200000)
            supplier_car.save()

    def _generate_carshowrooms(self):
        for i in range(10):
            self._generate_carshowroom()

    def _generate_carshowroom(self):
        charact1 = random.choice(list(DefaultCharacteristics))
        charact2 = random.choice(list(DefaultCharacteristics))
        return CarshowroomModel.objects.get_or_create(
            name=self.generate_random_string(random.randint(4, 10)),
            location=random.choice(list(dict(countries))),
            balance=random.randint(500000, 1000000),
            car_characteristic={
                charact1.name: charact1.value,
                charact2.name: charact2.value
            },
            client_discount=random.randint(0, 10),
            number_of_prod=random.randint(20, 500),
        )

    def _generate_suppliers_discounts(self):
        self._generate_discounts(SupplierModel, DiscountModel)

    def _generate_carshowroom_discounts(self):
        self._generate_discounts(CarshowroomModel, CarshowroomDiscountModel)

    def _generate_discounts(self, entity_class, discount_entity_class):
        min_id = entity_class.objects.aggregate(Min('id'))['id__min']
        max_id = entity_class.objects.aggregate(Max('id'))['id__max']
        min_car_id = CarModel.objects.aggregate(Min('id'))['id__min']
        max_car_id = CarModel.objects.aggregate(Max('id'))['id__max']
        for i in range(10):
            if entity_class == SupplierModel:
                discount, created = discount_entity_class.objects.get_or_create(
                    supplier=entity_class.objects.get(id=random.randint(
                        min_id,
                        max_id
                    )),
                    time_start=datetime.now().date(),
                    time_end=datetime.now().date() + timedelta(weeks=2),
                    name=self.generate_random_string(random.randint(4, 10)),
                    percent=random.randint(0, 20),

                )
            else:
                discount, created = discount_entity_class.objects.get_or_create(
                    carshowroom=entity_class.objects.get(id=random.randint(
                        min_id,
                        max_id
                    )),
                    time_start=datetime.now().date(),
                    time_end=datetime.now().date() + timedelta(weeks=2),
                    name=self.generate_random_string(random.randint(4, 10)),
                    percent=random.randint(0, 20),

                )
            if created:
                for j in range(random.randint(0, 5)):
                    discount.car.add(CarModel.objects.get(id=random.randint(
                        min_car_id,
                        max_car_id
                    )))

    def generate_random_string(self, length):
        symbols = string.ascii_uppercase + '1234567890'
        rand_string = ''.join(random.choice(symbols) for i in range(length))
        return rand_string
