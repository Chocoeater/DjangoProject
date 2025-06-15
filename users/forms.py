from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "avatar", "phone", "country", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "example@mail.ru"}
        )
        self.fields["avatar"].widget.attrs.update({"class": "form-control"})
        self.fields["phone"].widget.attrs.update({"class": "form-control"})
        self.fields["country"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        fields = ["avatar", "phone", "country"]
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    password = None
