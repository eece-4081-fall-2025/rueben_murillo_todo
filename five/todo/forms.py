from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['name', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeUnput(attrs={'type': 'datetime-local'}),
        }