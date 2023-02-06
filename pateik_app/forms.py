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

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = Customer
        fields  = (
            "username",
            "image",
            "password1",
            "password2",

        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "input--style-3", "placeholder": "Имя"}),
            "image": forms.FileInput(attrs={'style':'display: none;','class':'btn btn--pill btn--green', 'required': True, }
         )
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Error"
            )
        return password2