from django import forms
from django.forms import CheckboxSelectMultiple

from mailing.models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "example@mail.ru"}
        )
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Иванов Иван Иванович"}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Текст..."}
        )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Текст..."}
        )
        self.fields["body"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Текст..."}
        )


class MailingForm(forms.ModelForm):
    recipient = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=CheckboxSelectMultiple(),
        label="Получатели",
    )

    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "recipient"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipient"].label_from_instance = lambda obj: obj.full_name
        self.fields["message"].label_from_instance = lambda obj: obj.subject

class BlockMailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].label_from_instance = lambda obj: obj.subject