from pytest_lazyfixture import lazy_fixture
from django.forms.models import model_to_dict
import pytest

from src.core.services import UsersService


user_service = UsersService()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    ['/api/user/', '/api/cars/', '/api/carshowroom/', '/api/customers/', '/api/suppliers/'])
def test_get_list(url, client):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/user/', lazy_fixture('user')),
        ('/api/cars/', lazy_fixture('car')),
        ('/api/carshowroom/', lazy_fixture('carshowroom')),
        ('/api/customers/', lazy_fixture('user')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_get_entity(url, entity, client):
    response = client.get(url + str(entity.id) + '/')
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/cars/', lazy_fixture('car')),
        ('/api/carshowroom/', lazy_fixture('carshowroom')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_create_entity(url, entity, client):
    response = client.post(url, model_to_dict(entity))
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/user/', lazy_fixture('user')),
        ('/api/cars/', lazy_fixture('car')),
        ('/api/carshowroom/', lazy_fixture('carshowroom')),
        ('/api/customers/', lazy_fixture('user')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_delete_entity(url, entity, client):
    response = client.delete(url + str(entity.id) + '/')
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url,entity',
    [
        ('/api/carshowroom/', lazy_fixture('carshowroom')),
        ('/api/customers/', lazy_fixture('user')),
        ('/api/suppliers/', lazy_fixture('supplier'))
    ]
)
def test_get_statistics(url, entity, client):
    response = client.get(url + str(entity.id) + '/get_statistics/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register(client):
    user_dc = {
        'username': 'TestUser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testemail@gmail.com',
        'password': 'test_password1234'
    }
    response = client.post('/api/user/register/', user_dc)
    assert response.status_code == 201


@pytest.mark.django_db
def test_send_restore_password_email(user, client):
    data = {
        'email': user.email
    }
    response = client.post('/api/user/send_restore_password_email/', data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_restore_password(user, client):
    data = {
        'password': 'testtststst123',
        'password_2': 'testtststst123'
    }
    response = client.post('/api/user/restore_password/' + user_service.get_tokens_for_user(user)['access'], data)
    assert response.status_code == 202


@pytest.mark.django_db
def test_send_confirm_email(user, client):
    client.credentials(HTTP_AUTHORIZATION='JWT ' + user_service.get_tokens_for_user(user)['access'])
    response = client.get('/api/user/send_confirm_email/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_confirm_email(user, client):
    response = client.get('/api/user/confirm_email/' + user_service.get_tokens_for_user(user)['access'] + '/')
    assert response.status_code == 200
