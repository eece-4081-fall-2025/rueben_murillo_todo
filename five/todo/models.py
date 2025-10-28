from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class ToDo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos',blank=True)
 

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['due_date']
        verbose_name = 'To-Do'
        verbose_name_plural = 'To-Dos'
        
    def mark_complete(self):
        self.completed = True
        self.save()
    
    def mark_incomplete(self):
        self.completed = False
        self.save()
    
    def is_overdue(self):
        if self.due_date and not self.completed:
            return timezone.now().date() > self.due_date
        return False