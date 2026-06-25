from django import forms
from .models import Task, TaskDetails


class TaskForm(forms.ModelForm):
    description = forms.CharField(
        max_length=200, 
        required=False, 
        label="Описание",
        widget=forms.TextInput(attrs={"placeholder": "Краткое описание"})
    )
    estimated_hours = forms.IntegerField(
        required=False, 
        label="Предполагаемые часы",
        widget=forms.NumberInput(attrs={"placeholder": "Часы", "min": 0})
    )

    class Meta:
        model = Task
        fields = ["title", "priority", "category", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название задачи"}),
            "priority": forms.NumberInput(attrs={"min": 1, "max": 3}),
            "category": forms.Select(),
            "tags": forms.SelectMultiple(),
        }

    def save(self, commit=True):
        task = super().save(commit=commit)
        
        details, created = TaskDetails.objects.get_or_create(task=task)
        
        details.description = self.cleaned_data.get('description', '')
        details.estimated_hours = self.cleaned_data.get('estimated_hours')
        
        if commit:
            details.save()
        return task