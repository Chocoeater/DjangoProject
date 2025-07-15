from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from users.apps import UsersConfig


class OwnerOrSuperPermMixin(UserPassesTestMixin):
    app_name = UsersConfig.name

    def test_func(self):
        user = self.request.user

        if user.is_superuser:
            return True

        if hasattr(self, "get_object"):
            obj = self.get_object()
            if obj == user:
                return True

        return False

    def handle_no_permission(self):
        raise PermissionDenied("Доступ запрещен")
