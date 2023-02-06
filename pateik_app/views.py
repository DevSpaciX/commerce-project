from datetime import datetime

import stripe
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin

from pateik_app.forms import PaymentForm, CustomUserCreationForm
from pateik_app.models import TrainingPlan, Training, Time, Day, Customer
from pateik_core import settings


# Create your views here.


def main_page(request):
    training_plan = TrainingPlan.objects.all()
    context = {"plan": training_plan}
    return render(request, template_name="index.html", context=context)


class AboutPage(generic.TemplateView):
    template_name = "about.html"


def payment_view(request, pk):
    train = TrainingPlan.objects.get(pk=pk)
    form = PaymentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            YOUR_DOMAIN = "http://127.0.0.1:8000/"

            day = datetime.strptime(str(form.cleaned_data.get("day")),"%d %b, %Y")
            day = day.strftime("%Y-%m-%d")
            name = form.cleaned_data.get("name")
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
        plan = session["metadata"]["plan_id"]
        Training.objects.create(
            name=username , social=social,day_train=str(day),time_train=str(time),plan_id=plan
        )
        Time.objects.filter(day__date=day).all().filter(time_start__hour=time).delete()
        if not Time.objects.filter(day__date=day).all():
            Day.objects.filter(date=day).delete()
    return HttpResponse(status=200)



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
        form = CustomUserCreationForm(request.POST or None)
        if not form.is_valid():
            # print(form)
            print(form.errors)
            context = {'errors':dict(form.errors)}
            return render(request, "registration/registration.html", context=context)
        else:
            form.save(self)
            username = self.request.POST["username"]
            password = self.request.POST["password1"]
            image = self.request.FILES
            user = authenticate(username=username, password=password, image=image)
            login(self.request, user)
            return HttpResponseRedirect(reverse("pateik:main-page"))

        # return render(request,"registration/registration.html")



    # def get_context_data(self, **kwargs):
    #     context = super(CreateUser, self).get_context_data(**kwargs)
    #     context['password1'] = self.
    #     return context

    # def form_valid(self, form):
    #     form.save()
    #     username = self.request.POST["username"]
    #     password = self.request.POST["password1"]
    #     image = self.request.FILES
    #     user = authenticate(username=username, password=password, image=image)
    #     login(self.request, user)
    #     return HttpResponseRedirect(reverse("pateik:main-page"))
    #
    # def form_invalid(self, form):
    #     self.extra_context["password1_errors"] = form.errors
    #     return HttpResponseRedirect(reverse("pateik:register-page"))

class Profile(generic.TemplateView):
    template_name = "profile.html"
    # def get(self, request, *args, **kwargs):
    #     user = request.user.username
    #     context = {"user":user}
    #     return render(request,context=context)

