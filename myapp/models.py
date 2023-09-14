from django.db import models
from django.utils import timezone

class Parent(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Attendance(models.Model):
    child = models.ForeignKey(Child, to_field="id", on_delete=models.CASCADE)
    attendance = models.CharField(max_length=10, default="2")
    reason = models.CharField(max_length=200, default="")
    datetime = models.DateTimeField(default=timezone.now())
    reply = models.CharField(max_length=200, default="")
    # date = models.DateTimeField(default=timezone.now().date())
    def __str__(self):
        return f"{self.child}_attendance_{timezone.now().date()}"