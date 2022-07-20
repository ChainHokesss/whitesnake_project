import pytest
import random
import json
from datetime import datetime
from rest_framework.test import APIClient, APIRequestFactory

from src.core.services import UsersService, CarsService
from src.core.models import Brands, BodyTypes, FuelTypes
from src.carshowroom.services import CarshowroomServices
from src.suppliers.services import SuppliersService

user_service = UsersService()
car_service = CarsService()
carshowroom_service = CarshowroomServices()
supplier_service = SuppliersService()

@pytest.fixture
def user():
    user_dc = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password1234',
        'email_is_confirmed': True
    }

    user = user_service.create_user(user_dc)
    return user

@pytest.fixture
def car():
    car_dc = {
        'brand': random.choice(list(Brands)).value,
        'body_type': random.choice(list(BodyTypes)).value,
        'fuel_type': random.choice(list(FuelTypes)).value,
        'issue_year': random.randint(1990, datetime.now().year),
        'model': 'T2',
        'mileage': random.randint(0, 100000),
    }

    car = car_service.create_car(car_dc)
    return car


@pytest.fixture
def carshowroom():
    carshowroom_dc = {
        'name': 'TestCarshowroom',
        'location': 'HM',
        'balance': 1000000,
        'car_characteristic': json.dumps({"mileage__lte": 22315}),
        'client_discount': 5,
        'number_of_prod': 100
    }

    return carshowroom_service.create_carshowroom(carshowroom_dc)


@pytest.fixture
def supplier():
    supplier_dc = {
        'name': 'TestSupplier',
        'foundation_date': 1990,
        'client_discount': 5,
        'number_of_prod': 100,
        'balance': 0
    }

    return supplier_service.create_supplier(supplier_dc)

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def factory():
    return APIRequestFactory()