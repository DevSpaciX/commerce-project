from datetime import datetime
from django.db import models


class Day(models.Model):
    date = models.DateField(default=datetime.now().strftime("%d %b, %Y"))

    def __str__(self):
        return self.date.strftime("%d %b, %Y")


class Time(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time_start = models.TimeField()

    def __str__(self):
        return self.time_start.strftime("%H:%M")


class TrainingPlan(models.Model):
    plan = models.CharField(max_length=15)
    price = models.PositiveIntegerField(default="20")

    def __str__(self):
        return self.plan


class Payment(models.Model):
    name = models.CharField(max_length=15, null=False)
    discord = models.CharField(max_length=30, null=False)
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, null=True)
    time = models.ForeignKey(Time, on_delete=models.SET_NULL, null=True)
    price = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)


class Training(models.Model):
    name = models.CharField(max_length=35)
    social = models.CharField(max_length=35)
    day_train = models.CharField(max_length=10)
    time_train = models.CharField(max_length=10)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.plan}"
