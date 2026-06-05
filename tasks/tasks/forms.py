from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(label="Название задачи", max_length=200)
    priority = forms.IntegerField(label="Приоритет", min_value=1, max_value=3, initial=1, required=False)