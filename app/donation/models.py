# app/donation/models.py

from django.db import models
from django.contrib.auth.models import User
from app.stream.models import Stream

class Donation(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('gateway', 'Gateway'), ('manual', 'Manual')])
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
