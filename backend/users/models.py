# Create your models here.
# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_activated = models.BooleanField(default=False)
    activation_link = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=100, default='profileIcon.png')
    
    # Связи
    friends = models.ManyToManyField('self', symmetrical=False)
    projects = models.ManyToManyField('api.Project', related_name='members')
    teams = models.ManyToManyField('api.Team', related_name='members')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email