from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.title
    

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    

class TaskDetails(models.Model):
    task = models.OneToOneField('tasks.Task', on_delete=models.CASCADE, verbose_name="Задача", related_name="details")
    description = models.CharField(max_length=200, verbose_name="Описание")
    estimated_hours = models.IntegerField(null=True, blank=True, verbose_name="Предполагаемые часы")

    def __str__(self):
        return f"Детали задачи: {self.task.title}"
