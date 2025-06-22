
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from mailing.apps import MailingConfig

# class MailingManagerAndOwnerPermMixin:
#     """Миксин для ограничения прав доступа всем, кроме менеджеров рассылок, суперпользователей и владельцев"""
#
#     def has_permission(self):
#         """Проверяет наличие прав"""
#         return (self.request.user.is_authenticated and (self.request.user.groups.filter(
#             name="Менеджер рассылок").exists() or self.request.user.is_superuser))
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if self.has_permission():
#             return queryset
#         return queryset.filter(owner=self.request.user)
#
#
# class OwnerPermMixin:
#     """Миксин для ограничения прав доступа всем, кроме суперпользователей и владельцев"""
#
#     def has_permission(self, obj):
#         """Проверяет наличие прав"""
#         return (self.request.user.is_authenticated and (
#                     self.request.user.is_superuser or obj.owner == self.request.user))
#
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         if self.has_permission(obj):
#             return obj
#         raise PermissionDenied


class OwnerOrManagerPermMixin(UserPassesTestMixin):
    app_name = MailingConfig.name
    base_perm = 'view'
    custom_perm = []

    def get_perms(self):
        model_name = self.model._meta.model_name
        perms = [f'{self.app_name}.{self.base_perm}_{model_name}']
        perms += self.custom_perm
        return perms

    def test_func(self):
        user = self.request.user

        if user.is_superuser:
            return True

        for perm in self.get_perms():
            if user.has_perm(perm):
                return True

        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if obj.owner == user:
                return True

        return False

    def handle_no_permission(self):
        raise PermissionDenied('Доступ запрещен')