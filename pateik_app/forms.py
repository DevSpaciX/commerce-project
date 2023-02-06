from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from pateik_app.models import Payment, Time, Customer


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("name", "discord", "day", "time")
        widgets = {
            "name": forms.TextInput(attrs={"class": "input--style-3","placeholder":"Имя"}),
            "discord": forms.TextInput(attrs={"class": "input--style-3","placeholder":"Telegram"}),
            "day": forms.Select(attrs={"class": "input--style-3","type":"date"}),
            "time": forms.Select(attrs={"class": "input--style-3", "type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time"].queryset = Time.objects.none()
        self.fields['day'].empty_label = "Выберите день"

        if "day" in self.data:
            try:
                day_id = int(self.data.get("day"))
                self.fields["time"].queryset = Time.objects.filter(day_id=day_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["time"].queryset = self.instance.country.time_set

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = UserCreationForm.Meta.fields = (
            "username",
            "image",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "input--style-3", "placeholder": "Имя"}),
            "image": forms.FileInput(attrs={'style':'display: none;','class':'btn btn--pill btn--green', 'required': True, }
         )
        }
