from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.forms import CustomResetPasswordForm, CustomSetPasswordForm
from users.views import (
    ChangeUserView,
    CustomLoginView,
    CustomLogoutView,
    ProfileUserView,
    RegisterView, UserListView, UserStatusToggle,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("user/<int:pk>/", ProfileUserView.as_view(), name="profile"),
    path("user/update/<int:pk>/", ChangeUserView.as_view(), name="update_user"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            form_class=CustomResetPasswordForm,
            template_name="reset_password/reset.html",
            success_url=reverse_lazy("users:reset_done"),
        ),
        name="reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="reset_password/done.html"),
        name="reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm,
            template_name="reset_password/confirm.html",
            success_url=reverse_lazy("users:reset_complete"),
        ),
        name="reset_confirm",
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(template_name="reset_password/complete.html"),
        name="reset_complete",
    ),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('change_user_status/<int:pk>/', UserStatusToggle.as_view(), name='change_status'),
]
