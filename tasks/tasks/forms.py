from django import forms

from .models import Task


# class TaskForm(forms.Form):
    # title = forms.CharField(label="Название задачи", max_length=200)
    # priority = forms.IntegerField(label="Приоритет", min_value=1, max_value=3, initial=1, required=False)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название задачи"}),
            "priority": forms.NumberInput(attrs={"placeholder": "Приоритет", "min": 1, "max": 3}),
        }
        


