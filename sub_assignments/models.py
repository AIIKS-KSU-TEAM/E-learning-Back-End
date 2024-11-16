from rest_framework import serializers
from django.db import models
from courses.models import Module
from django.utils import timezone

class Assignment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assignments/')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return self.title

    def is_past_deadline(self):
        return self.deadline and timezone.now() > self.deadline