from django.contrib import admin
from mailing.models import Recipient, Message, Mailing

# Register your models here.


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "comment")
    search_fields = ("email", "full_name", "comment")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject", "body")

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("start_time", "end_time", "status", "message", "get_recipient")
    search_fields = ("message", "recipient")
    list_filter = ('status',)

    def get_recipient(self, obj):
        return ", ".join([str(recipient) for recipient in obj.recipient.all()])
    get_recipient.short_description = "Recipients"
