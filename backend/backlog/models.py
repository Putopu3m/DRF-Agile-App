# api/models.py
from django.db import models
from sprints.models import Sprint  # Импорт модели Sprint из предыдущего шага

class BacklogIdeaItem(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    data = models.TextField(default='')
    is_tasked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} ({self.priority})"

class BacklogIdea(models.Model):
    name = models.CharField(max_length=255, default='')
    items = models.ManyToManyField(BacklogIdeaItem, related_name='backlog_ideas')
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name