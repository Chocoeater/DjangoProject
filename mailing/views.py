from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.mixins import MailingManagerAndOwnerPermMixin, OwnerPermMixin
from mailing.models import Attempt, Mailing, Message, Recipient

# Create your views here.


class RecipientListView(MailingManagerAndOwnerPermMixin, ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"


class RecipientDetailView(OwnerPermMixin, DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_create.html"
    success_url = reverse_lazy("mailing:recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(OwnerPermMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    context_object_name = "recipient"
    template_name = "recipient_update.html"

    def get_success_url(self):
        return reverse("mailing:recipient", kwargs={"pk": self.object.pk})


class RecipientDeleteView(OwnerPermMixin, DeleteView):
    model = Recipient
    template_name = "recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("mailing:recipients_list")


class MessageListView(MailingManagerAndOwnerPermMixin, ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageDetailView(OwnerPermMixin, DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "message_create.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerPermMixin, UpdateView):
    model = Message
    template_name = "message_update.html"
    context_object_name = "message"
    form_class = MessageForm

    def get_success_url(self):
        return reverse("mailing:message", kwargs={"pk": self.object.pk})


class MessageDeleteView(OwnerPermMixin, DeleteView):
    model = Message
    template_name = "message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing:messages_list")


class MailingListView(MailingManagerAndOwnerPermMixin, ListView):
    model = Mailing
    template_name = "mailings_list.html"
    context_object_name = "mailings"


class MailingDetailView(OwnerPermMixin, DetailView):
    model = Mailing
    template_name = "mailing_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailing_create.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(OwnerPermMixin, UpdateView):
    model = Mailing
    template_name = "mailing_update.html"
    form_class = MailingForm

    def get_success_url(self):
        return reverse("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(OwnerPermMixin, DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("mailing:mailings_list")


@require_POST
def mailing_run_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.status != "started":
        mailing.start_time = timezone.now()
        mailing.end_time = mailing.start_time + timedelta(minutes=2)
        mailing.save()
        mailing.send()
        messages.success(request, "Рассылка запущена!")
    else:
        messages.warning(request, "Рассылка уже запущена!")
    return redirect("mailing:mailings_list")


@require_POST
def mailing_update_status_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.save()
    messages.success(request, "Готово!")
    return redirect("mailing:mailings_list")


class AttemptListView(MailingManagerAndOwnerPermMixin, ListView):
    model = Attempt
    template_name = "attempts_list.html"
    context_object_name = "attempts"


class MianPageView(TemplateView):
    template_name = "mailing_home.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_superuser or user.groups.filter(name="Менеджер рассылок").exists():
            context["total_mailings"] = Mailing.objects.count()
            context["total_active"] = Mailing.objects.filter(status="started").count()
            context["recipients"] = Recipient.objects.count()
        else:
            context["total_mailings"] = Mailing.objects.filter(owner=user).count()
            context["total_active"] = Mailing.objects.filter(status="started", owner=user).count()
            context["recipients"] = Recipient.objects.filter(owner=user).count()
        return context
