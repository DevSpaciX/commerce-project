from django.contrib import admin

from pateik_app.models import Day, AvailableTime, Payment, TrainingPlan, Training, Customer,AvailableSlots

admin.site.register(Day)
admin.site.register(AvailableTime)
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(Training)
admin.site.register(TrainingPlan)
admin.site.register(AvailableSlots)


