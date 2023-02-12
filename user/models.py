from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    safe = models.BooleanField(default=False)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.ManyToManyField(Employee)
    name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)


