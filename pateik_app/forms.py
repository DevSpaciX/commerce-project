from datetime import datetime
import os
import tempfile
from django import forms
from django.core.exceptions import ValidationError
from django.core.files import File
from storages.backends import dropbox

from pateik_app.models import Payment, AvailableTime, Customer
from pateik_core import settings


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("discord", "day", "time")
        widgets = {
            # "name": forms.TextInput(attrs={"class": "input--style-3","placeholder":"Имя"}),
            "discord": forms.TextInput(
                attrs={"class": "input--style-3", "placeholder": "Telegram/Discord"}
            ),
            "day": forms.Select(attrs={"class": "input--style-3", "type": "date"}),
            "time": forms.Select(attrs={"class": "input--style-3", "type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time"].queryset = AvailableTime.objects.none()
        self.fields["day"].empty_label = "Choose day"

        if "day" in self.data:
            try:
                day_id = int(self.data.get("day"))
                self.fields["time"].queryset = AvailableTime.objects.filter(day_id=day_id)
            except (ValueError, TypeError):
                pass

    def clean_discord(self):
        discord = self.cleaned_data.get("discord")
        if len(discord) > 15:
            raise ValidationError("Your contact data is too long")
        return discord


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = (
            "username",
            "image",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "input--style-3", "placeholder": "Name"}
            ),
            "image": forms.FileInput(
                attrs={
                    "style""class":"btn btn-outline-secondary btn-lg","required":True
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords must match")
        if len(password1) < 7:
            raise ValidationError("Password should contain minimum 8 characters")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # зберігаємо фото на DropBox
            access_token = settings.DROPBOX_APP_KEY
            dbx = dropbox.Dropbox(access_token)

            image = self.cleaned_data.get('image')
            if image:
                image_path = f"/images/{user.pk}_{image.name}"
                dbx.files_upload(image.read(), image_path)

            # оновлюємо поле зображення в об'єкті користувача
            user.customer.image = image_path
            user.customer.save()

        return user
