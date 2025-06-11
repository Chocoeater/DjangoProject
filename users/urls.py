from django.urls import path

from users.apps import UsersConfig
from users.views import (ChangeUserView, CustomLoginView, CustomLogoutView,
                         ProfileUserView, RegisterView)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("user/<int:pk>", ProfileUserView.as_view(), name="profile"),
    path("user/update/<int:pk>", ChangeUserView.as_view(), name="update_user"),
]
