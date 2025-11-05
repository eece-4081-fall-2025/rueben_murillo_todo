from django import forms
from .models import ToDo,Project

class ToDoForm(forms.ModelForm):
    due_date = forms.DateField(
        required = False,
        widget=forms.DateInput(attrs={'type':'date'},format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'])
    class Meta:
        model = ToDo
        fields = ['name', 'description', 'due_date', 'completed', 'priority', 'project']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(user=user)
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']