from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def completion_percent(self):
        total = self.todos.count()
        done = self.todos.filter(completed=True).count()
        return int(done / total *100) if total else 0
    
    def __str__(self):
        return self.name


class ToDo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.PositiveSmallIntegerField(default=3, choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')])
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
        
    def mark_complete(self):
        self.completed = True
        self.save()
    
    def mark_incomplete(self):
        self.completed = False
        self.save()
    
    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
    
    class Meta:
        ordering = ['priority', 'due_date', 'created_at']