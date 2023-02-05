from django.shortcuts import render
from django.views import generic

from pateik_app.models import TrainingPlan


# Create your views here.


def main_page(request):
    training_plan = TrainingPlan.objects.all()
    context = {"plan": training_plan}
    return render(request, template_name="index.html", context=context)


class AboutPage(generic.TemplateView):
    template_name = "about.html"
