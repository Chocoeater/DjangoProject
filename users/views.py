from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from users.forms import (CustomLoginForm, CustomUserChangeForm, CustomUserCreationForm)
from users.mixins import OwnerOrSuperPermMixin
from users.models import User


# Create your views here.


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:product_list")


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать!"
        message = "Вам здесь (не) рады!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email, ]
        send_mail(subject, message, from_email, recipient_list)


class ChangeUserView(OwnerOrSuperPermMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    context_object_name = "user"
    template_name = "user_update.html"


    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.object.pk})


class ProfileUserView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        perm = f'{obj._meta.app_label}.view_{obj._meta.model_name}'

        if user.is_superuser or user.has_perm(perm) or user == obj:
            return obj
        else:
            raise PermissionDenied

class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users_list.html'
    ordering = ['pk']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.has_perm('users.view_user'):
            return User.objects.exclude(pk=user.pk).order_by('pk')
        else:
            raise PermissionDenied

class UserStatusToggle(View):
    def post(self, request, pk):
        if not (request.user.is_superuser or request.user.has_perm('users.can_block_user')):
            raise PermissionDenied

        user_obj = get_object_or_404(User, pk=pk)

        if user_obj == request.user or user_obj.is_superuser:
            pass
        else:
            user_obj.is_active = not user_obj.is_active
            user_obj.save()

        return redirect('users:users_list')