from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import login
from django.conf import settings
from users.models import User

from users.forms import CustomUserCreationForm, CustomLoginForm, CustomUserChangeForm


# Create your views here.

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:product_list')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать!'
        message = 'Вам здесь (не) рады!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email,]
        send_mail(subject, message, from_email, recipient_list)

class ChangeUserView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    context_object_name = 'user'
    template_name = 'user_update.html'

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.object.pk})

class ProfileUserView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user_detail.html'