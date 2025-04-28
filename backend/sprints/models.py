# api/models.py
from django.db import models
from users.models import User

class ProsConsBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Pros(ProsConsBase):
    pass

class Cons(ProsConsBase):
    pass

class Sprint(models.Model):
    name = models.CharField(max_length=255, default='')
    tasks = models.ManyToManyField('Task', related_name='sprints')
    duration = models.IntegerField(default=2)
    days = models.JSONField(default=list)  # Для хранения массива чисел
    pros = models.ManyToManyField(Pros, related_name='sprint_pros')
    cons = models.ManyToManyField(Cons, related_name='sprint_cons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name