from datetime import timedelta

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone


from mailing.models import Recipient, Message, Mailing, Attempt
from mailing.forms import RecipientForm, MessageForm, MailingForm
# Create your views here.

class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'recipient_detail.html'
    context_object_name = 'recipient'

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipient_create.html'
    success_url = reverse_lazy('mailing:recipients_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    context_object_name = 'recipient'
    template_name = 'recipient_update.html'

    def get_success_url(self):
        return reverse("mailing:recipient", kwargs={"pk": self.object.pk})

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'recipient_delete.html'
    context_object_name = 'recipient'
    success_url = reverse_lazy('mailing:recipients_list')

class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

class MessageCreateView(CreateView):
    model = Message
    template_name = 'message_create.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')

class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'message_update.html'
    context_object_name = 'message'
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:message', kwargs={"pk": self.object.pk})

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:messages_list')

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings_list.html'
    context_object_name = 'mailings'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing_create.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing_update.html'
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_delete.html'
    success_url = reverse_lazy('mailing:mailings_list')

@require_POST
def mailing_run_view(request, pk):
    print("mailing_run_view called")
    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.status != 'started':
        mailing.start_time = timezone.now()
        mailing.end_time = mailing.start_time + timedelta(minutes=2)
        mailing.save()
        mailing.send()
        messages.success(request, 'Рассылка запущена!')
    else:
        messages.warning(request, 'Рассылка уже запущена!')
    return redirect('mailing:mailings_list')

@require_POST
def mailing_update_status_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.save()
    messages.success(request, 'Готово!')
    return redirect('mailing:mailings_list')

class AttemptListView(ListView):
    model = Attempt
    template_name = 'attempts_list.html'
    context_object_name = 'attempts'

class MianPageView(TemplateView):
    template_name = 'mailing_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['total_active'] = Mailing.objects.filter(status='started').count()
        context['recipients'] = Recipient.objects.count()
        return context

