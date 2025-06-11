from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.conf import settings

from users.forms import CustomUserCreationForm, CustomLoginForm


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