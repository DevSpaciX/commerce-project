from django import forms
from django.core.exceptions import ValidationError


from pateik_app.models import Payment, Time, Customer


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
        self.fields["time"].queryset = Time.objects.none()
        self.fields["day"].empty_label = "Выберите день"

        if "day" in self.data:
            try:
                day_id = int(self.data.get("day"))
                self.fields["time"].queryset = Time.objects.filter(day_id=day_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["time"].queryset = self.instance.country.time_set

    def clean_discord(self):
        discord = self.cleaned_data.get("discord")
        if len(discord) > 15:
            raise ValidationError("Ваши контакты слишком длинные")
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
                    "style": "display: none;",
                    "required": True,
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли должны совпадать")
        if len(password1) < 7:
            raise ValidationError("Пароль должен иметь 8 символов")
        return password2
