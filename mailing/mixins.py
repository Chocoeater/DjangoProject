from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from mailing.apps import MailingConfig


class OwnerOrManagerPermMixin(UserPassesTestMixin):
    app_name = MailingConfig.name
    base_perm = "view"
    custom_perm = []

    def get_perms(self):
        model_name = self.model._meta.model_name
        perms = [f"{self.app_name}.{self.base_perm}_{model_name}"]
        perms += self.custom_perm
        return perms

    def test_func(self):
        user = self.request.user

        if user.is_superuser:
            return True

        for perm in self.get_perms():
            if user.has_perm(perm):
                return True

        if hasattr(self, "get_object"):
            obj = self.get_object()
            if obj.owner == user:
                return True

        return False

    def handle_no_permission(self):
        raise PermissionDenied("Доступ запрещен")
