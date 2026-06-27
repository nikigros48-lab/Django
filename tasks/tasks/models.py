from django.db import models
from django.contrib.auth.models import User
    

class Task(models.Model):
    title = models.CharField("Название задачи", max_length=255)
    completed = models.BooleanField("Завершена", default=False)
    priority = models.IntegerField("Приоритет", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="tasks")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги", related_name="tasks")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
    

class TaskDetails(models.Model):
    task = models.OneToOneField('Task', on_delete=models.CASCADE, verbose_name="Задача", related_name="details")
    description = models.CharField(max_length=200, verbose_name="Описание")
    estimated_hours = models.IntegerField(null=True, blank=True, verbose_name="Предполагаемые часы")

    class Meta:
        verbose_name = "Детали задачи"
        verbose_name_plural = "Детали задач"

    def __str__(self):
        return f"Детали задачи: {self.task.title}"
    

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title
    

class Commentary(models.Model):
    description = models.CharField("Описание", max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Задача")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.description

