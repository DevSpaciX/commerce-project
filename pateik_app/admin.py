from django.contrib import admin

from pateik_app.models import Day, Time, Payment, TrainingPlan, Training

admin.site.register(Day)
admin.site.register(Time)
admin.site.register(Payment)
admin.site.register(Training)
admin.site.register(TrainingPlan)