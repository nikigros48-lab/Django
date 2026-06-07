from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
    

class Task(models.Model):
    title = models.CharField("Название задачи", max_length=255)
    completed = models.BooleanField("Завершена", default=False)
    priority = models.IntegerField("Приоритет", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="tasks")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

