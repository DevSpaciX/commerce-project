from django.contrib import admin

from pateik_app.models import Day, DateTime, Payment, TrainingPlan, Training, Customer

admin.site.register(Day)
admin.site.register(DateTime)
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(Training)
admin.site.register(TrainingPlan)

