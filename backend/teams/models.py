# api/models.py
from django.db import models
from users.models import User

class Team(models.Model):
    name = models.CharField(max_length=255, default='')
    users = models.ManyToManyField(User, related_name='teams')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name