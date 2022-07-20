import pytest

@pytest.mark.django_db
def test_supplier_car_create(supplier, car, client):
    data = {
        "is_active": True,
        "price": "12000",
        "supplier": supplier.id,
        "car": car.id
    }
    response = client.post('/api/supplier/cars/', data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_supplier_discount_create(supplier, car, client):
    data = {
        "supplier_id": supplier.id,
        "time_start": "2022-07-20",
        "time_end": "2022-07-20",
        "name": "string",
        "percent": 5,
        "car": [
            car.id
        ]
    }

    response = client.post('/api/supplier/discount/', data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_cars(supplier, car, client):
    supplier.car_list.add(car)
    supplier.save()
    response = client.get('/api/suppliers/' + str(supplier.id) + '/get_cars/')
    assert response.status_code == 200
