from django.core.exceptions import PermissionDenied


class MailingManagerAndOwnerPermMixin:
    """Миксин для ограничения прав доступа всем, кроме менеджеров рассылок, суперпользователей и владельцев"""

    def has_permission(self):
        """Проверяет наличие прав"""
        return (self.request.user.is_authenticated and (self.request.user.groups.filter(
            name="Менеджер рассылок").exists() or self.request.user.is_superuser))

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.has_permission():
            return queryset
        return queryset.filter(owner=self.request.user)


class OwnerPermMixin:
    """Миксин для ограничения прав доступа всем, кроме суперпользователей и владельцев"""

    def has_permission(self, obj):
        """Проверяет наличие прав"""
        return (self.request.user.is_authenticated and (
                    self.request.user.is_superuser or obj.owner == self.request.user))

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.has_permission(obj):
            return obj
        raise PermissionDenied
