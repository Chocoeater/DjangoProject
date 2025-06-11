from users.apps import UsersConfig
from django.urls import path
from users.views import CustomLoginView, CustomLogoutView, RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
]