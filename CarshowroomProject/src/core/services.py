from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail

from src.core.models import BaseUser, CarModel


class CarsService:
    def create_car(self, car_data):
        car = CarModel.objects.get_or_create(**car_data)
        return car[0]

    def get_car(self, car_id=None, car_data=None):
        if car_id != None:
            return get_object_or_404(CarModel, id=car_id)
        if car_data != None:
            return get_object_or_404(CarModel, **car_data)

        raise NotFound()

    def get_cars_by_characteristics(self, characteristics_dict):
        return CarModel.objects.filter(**characteristics_dict)


class UsersService:
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get_user_from_access_token(self, access_token_str):
        try:
            access_token_obj = AccessToken(access_token_str)
            user_id = access_token_obj['user_id']
            user = BaseUser.objects.get(id=user_id)
            return user
        except Exception as e:
            return None

    def get_user(self, user_id = None, email = None):
        if email:
            return get_object_or_404(BaseUser, email=email)
        if user_id:
            return get_object_or_404(BaseUser, id=user_id)
        else:
            return None

    def create_user(self, user_data):
        user = BaseUser(**user_data)
        user.set_password(user.password)
        user.save()

        return user

    def send_email(
            self,
            user,
            url = 'api/user/confirm_email/',
            title = 'Confirm email',
            message = f'To confirm your email. You should follow the link http://0.0.0.0:8000/'
    ):
        link = self.get_tokens_for_user(user)['access']
        send_mail(
            title,
            message + url + link + '.',
            'nazarkurilovic@gmail.com',
            [user.email],
            fail_silently=False,
        )

    def send_restore_password_email(self, user):
        self.send_email(
            user = user,
            url = 'api/user/restore_password/',
            title = 'Restore password',
            message = f'To restore your password. You should follow the link http://0.0.0.0:8000/'
        )

