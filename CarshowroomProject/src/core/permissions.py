from rest_framework.permissions import BasePermission


class EmailConfirmPermission(BasePermission):
    message = 'Users email does not confirmed.'

    def has_permission(self, request, view):
        return request.user.email_is_confirmed is True
