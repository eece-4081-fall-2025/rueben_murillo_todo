from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class ToDo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', blank=True, null=True)

    @property
    def is_overdue(self):
        return not self.completed and self.due_date and timezone.now().date() > self.due_date
    # class Meta:
    #     ordering = ['due_date']
    #     verbose_name = 'To-Do'
    #     verbose_name_plural = 'To-Dos'
        
    def mark_complete(self):
        self.completed = True
        self.save()
    
    def mark_incomplete(self):
        self.completed = False
        self.save()
    
    def __str__(self):
        return self.name