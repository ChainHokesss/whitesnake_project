from rest_framework.response import Response
from rest_framework import decorators, status
from rest_framework.permissions import IsAuthenticated

class UpdateProfileMixin:
    @decorators.action(methods = ['POST'], detail = False)
    @decorators.permission_classes([IsAuthenticated])
    def update_profile(self, request):
        instance = self.service.get_profile(user_id = request.user.id)
        serializer = self.get_serializer(instance, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(
            {instance.user.role: serializer.data},
            status = status.HTTP_202_ACCEPTED
        )

class GetProfileMixin:
    @decorators.action(methods = ['GET'], detail = False)
    @decorators.permission_classes([IsAuthenticated])
    def get_profile(self, request):
        instance = self.service.get_profile(user_id = request.user.id)
        return Response(
            {instance.user.role: self.get_serializer(instance).data},
            status = status.HTTP_200_OK
        )