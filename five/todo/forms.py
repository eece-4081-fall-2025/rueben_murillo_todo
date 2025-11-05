from django import forms
from .models import ToDo,Project

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        exclude = ['user']
        fields = ['name', 'description', 'due_date','priority','project']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description' : forms.Textarea(attrs={'rows':3}),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']