
from rest_framework import permissions

from .models import Account


class AccountExistPermission(permissions.BasePermission):
    message = 'An account with this name was not found.'

    def has_permission(self, request, view):
        account_name = view.kwargs.get('account_name')
        return Account.objects.filter(name=account_name).exists()

    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view)
