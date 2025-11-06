from django import forms
from .models import ToDo,Project

class ToDoForm(forms.ModelForm):
    due_date = forms.DateField(
        required = False,
        widget=forms.DateInput(attrs={'type':'date'}),
        input_formats=['%Y-%m-%d'],
    )
    #Test method for debugging
    # def clean_due_date(self):
    #     due_date = self.cleaned_data.get('due_date')
    #     print(f"DEBUG - due_date value : {due_date!r}")
    #     print(f"DEBUG - due_date type : {type(due_date)}")
    #     return due_date
    class Meta:
        model = ToDo
        fields = ['name', 'description', 'due_date', 'completed', 'priority', 'project']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(user=user)
            self.fields['priority'].initial = 3
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']