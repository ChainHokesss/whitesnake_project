import pytest

from src.core.services import UsersService

user_service = UsersService()

@pytest.mark.django_db
def test_create_offer(user, client):
    data = {
      "issue_year__gt": 2000,
      "mileage__lt": 90019
    }
    client.credentials(HTTP_AUTHORIZATION='JWT ' + user_service.get_tokens_for_user(user)['access'])
    response = client.post('/api/customers/create_offer', data)

    return response.status_code == 201