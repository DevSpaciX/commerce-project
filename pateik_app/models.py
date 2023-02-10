from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Day(models.Model):
    date = models.DateField(default=datetime.now().strftime("%d %b, %Y"))

    def __str__(self):
        return self.date.strftime("%d %b, %Y")


class AvailableTime(models.Model):
    slots = models.DateTimeField()

    def __str__(self):
        return self.slots.strftime("%d %b, %Y %H:%M")


class AvailableSlots(models.Model):
    slots = models.DateTimeField()

    def __str__(self):
        return self.slots.strftime("%d %b, %Y %H:%M")

class TrainingPlan(models.Model):
    plan = models.CharField(max_length=15)
    price = models.PositiveIntegerField(default="20")

    def __str__(self):
        return self.plan


class Payment(models.Model):
    name = models.CharField(max_length=15, null=False)
    discord = models.CharField(max_length=30, null=False)
    day = models.ForeignKey(AvailableSlots, on_delete=models.SET_NULL, null=True,related_name="training_day")
    time = models.ForeignKey(AvailableSlots, on_delete=models.SET_NULL, null=True,related_name="training_time")
    price = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE,related_name="training_price")


class Customer(AbstractUser):
    image = models.ImageField(upload_to="images/", default="hqdefault.jpg")
    training_paid = models.ForeignKey(
        TrainingPlan,
        on_delete=models.CASCADE,
        related_name="customers",
        null=True,
        blank=True,
    )


class Training(models.Model):
    name = models.CharField(max_length=35)
    social = models.CharField(max_length=35)
    day_train = models.CharField(max_length=10)
    time_train = models.CharField(max_length=10)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE,related_name="training_plan")

    def __str__(self):
        return f"{self.name} {self.plan}"
