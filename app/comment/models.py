# app/comment/models.py

from django.db import models
from django.contrib.auth.models import User
from app.stream.models import Stream

class Comment(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
