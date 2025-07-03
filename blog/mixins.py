from django.core.exceptions import PermissionDenied


class ContentManagerPermMixin:
    """Миксин для ограничения прав доступа всем, кроме контент-менеджеров и суперпользователей"""

    def has_permission(self):
        """Проверяет наличие прав"""
        return (
            self.request.user.groups.filter(name="Контент-менеджер").exists()
            or self.request.user.is_superuser
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.has_permission():
            return obj
        raise PermissionDenied
