from datetime import datetime

import stripe
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin

from pateik_app.forms import PaymentForm, CustomUserCreationForm
from pateik_app.models import TrainingPlan, Training, Time, Day, Customer, Payment
from pateik_core import settings


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def main_page(request):
    training_plan = TrainingPlan.objects.all()
    users = Customer.objects.all().count()
    context = {"plan": training_plan,"users":users}
    return render(request, template_name="index.html", context=context)


class AboutPage(generic.TemplateView):
    template_name = "about.html"


@login_required
def payment_view(request, pk):
    train = TrainingPlan.objects.get(pk=pk)
    form = PaymentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            YOUR_DOMAIN = "http://127.0.0.1:8000/"
            day = datetime.strptime(str(form.cleaned_data.get("day")),"%d %b, %Y")
            day = day.strftime("%Y-%m-%d")
            name = request.user.username
            discord = form.cleaned_data.get("discord")
            time = str(form.cleaned_data.get("time"))
            time = datetime.strptime(time,"%H:%M").time().strftime("%H")
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": train.price * 100,
                            "product_data": {
                                "name": train.plan,
                            },
                        },
                        "quantity": 1,
                    },
                ],
                metadata={
                    "day": day,
                    "time": time,
                    "username": name,
                    "discord": discord,
                    "plan_id": pk,
                },
                mode="payment",
                success_url=YOUR_DOMAIN + "/payment-success/",
                cancel_url=YOUR_DOMAIN + "/payment-denied/",
            )
            return redirect(checkout_session.url, code=303)
        return render(request, "payment_form.html", {"form": form,"errors":dict(form.errors),"train":train })
    return render(request, "payment_form.html", {"form": form,"train":train })

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        day = session["metadata"]["day"]
        time = session["metadata"]["time"]
        social = session["metadata"]["discord"]
        username = session["metadata"]["username"]
        plan_id = session["metadata"]["plan_id"]
        Training.objects.create(
            name=username , social=social,day_train=str(day),time_train=str(time),plan_id=plan_id
        )

        Time.objects.filter(day__date=day).filter(time_start__hour=time).delete()
        user = Customer.objects.get(username=username)
        user.training_paid_id = plan_id
        user.save()
        if not Time.objects.filter(day__date=day).all():
            Day.objects.filter(date=day).delete()
    return HttpResponse(status=200)

def payment_success(request):
    return render(request,"payment-success.html")


def payment_denied(request):
    return render(request,"payment-denied.html")

# AJAX
def load_times(request):
    day_id = request.GET.get("day")
    times = Time.objects.filter(day_id=day_id).all()
    return render(request, "drop_down_time.html", {"times": times})

class CreateUser(generic.View):
    def get(self,request):
        form = CustomUserCreationForm()
        context = {"form":form}
        return render(request,"registration/registration.html",context=context)
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if not form.is_valid():
            form = CustomUserCreationForm(request.POST)
            context = {'form':form,'errors':dict(form.errors)}
            return render(request, "registration/registration.html", context=context)
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        image = self.request.FILES
        user = authenticate(username=username, password=password, image=image)
        login(self.request, user)
        return HttpResponseRedirect(reverse("pateik:main-page"))

def login_view(request):
    if request.method == "GET":
        return render(request, "registration/login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("pateik:main-page"))
        error_context = {"errors": "invalid data"}
        return render(request, "registration/login.html", context=error_context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("pateik:main-page"))

class Profile(generic.TemplateView):
    template_name = "profile.html"


