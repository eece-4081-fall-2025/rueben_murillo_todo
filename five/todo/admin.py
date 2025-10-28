from django.contrib import admin
from .models import ToDo

# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed', 'due_date')
    list_filter = ('completed', 'due_date')
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Todo Details', {
            'fields': ('name', 'description', 'due_date')
        }),
        ('Status', {
            'fields': ('completed','overdue')
        }),)