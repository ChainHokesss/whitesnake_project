from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import decorators, status, exceptions
from rest_framework.generics import GenericAPIView

from .serializers import CarSerializer, UserSerializer, RestorePasswordSerializer
from .models import BaseUser, CarModel
from .services import UsersService


class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    # only admin
    permission_classes = (AllowAny, )
    queryset = CarModel.objects.all()
    service = UsersService()

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    # only admin
    permission_classes = (AllowAny, )
    queryset = BaseUser.objects.all()
    service = UsersService()

    @decorators.action(methods=('POST', ), detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.service.confirm_email(user)
        return Response(
            self.service.get_tokens_for_user(user),
            status=status.HTTP_200_OK
        )

    @decorators.action(methods=['GET'], detail=False)
    @decorators.permission_classes((IsAuthenticated, ))
    def send_confirm_email(self, request):
        self.service.send_email(request.user)
        return Response('OK')

    @decorators.action(methods=['GET'], detail=False, url_path=r'confirm_email/(?P<token>[\S-]+)')
    def confirm_email(self, request, token):
        user = self.service.get_user_from_access_token(token)
        if user:
            user.email_is_confirmed = True
            user.save()
            return Response("Email is confirmed")

        return Response("Error", status = status.HTTP_404_NOT_FOUND)

    @decorators.action(methods=('POST', ), detail=False)
    def send_restore_password_email(self, request):
        email = request.data.get('email')
        if not email:
            return exceptions.ParseError()

        user = self.service.get_user(email = email)
        self.service.send_restore_password_email(user)

        return Response("Mail was send")


class RestorePasswordView(GenericAPIView):
    serializer_class = RestorePasswordSerializer
    service =  UsersService()
    permission_classes = (AllowAny, )

    def post(self, request, token):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        password_1 = serializer.data['password']
        password_2 = serializer.data['password_2']
        user = self.service.get_user_from_access_token(token)
        if password_1 != password_2:
            return exceptions.ErrorDetail(detail = "passwords are not match")
        user.set_password(password_1)
        user.save()
        return Response("Password was changed")