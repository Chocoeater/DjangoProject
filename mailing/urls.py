from django.urls import path
from mailing.apps import MailingConfig

from mailing.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView, MessageListView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, mailing_run_view, \
    mailing_update_status_view, AttemptListView, MianPageView

app_name = MailingConfig.name

urlpatterns = [path('recipients', RecipientListView.as_view(), name='recipients_list'),
               path('recipient/<int:pk>', RecipientDetailView.as_view(), name='recipient'),
               path('recipient/create', RecipientCreateView.as_view(), name='recipient_create'),
               path('recipient/<int:pk>/update', RecipientUpdateView.as_view(), name='recipient_update'),
               path('recipient/<int:pk>/delete', RecipientDeleteView.as_view(), name='recipient_delete'),
               path('messages', MessageListView.as_view(), name='messages_list'),
               path('message/<int:pk>', MessageDetailView.as_view(), name='message'),
               path('message/create', MessageCreateView.as_view(), name='message_create'),
               path('message/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
               path('message/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
               path('mailings', MailingListView.as_view(), name='mailings_list'),
               path('mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
               path('mailing/create', MailingCreateView.as_view(), name='mailing_create'),
               path('mailing/<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
               path('mailing/<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),
               path('mailings/send/<int:pk>', mailing_run_view, name='mailing_run'),
               path('mailing/update_status/<int:pk>', mailing_update_status_view, name='mailing_status_update'),
               path('attempts/', AttemptListView.as_view(), name='attempts_list'),
               path('', MianPageView.as_view(), name='home')
               ]
