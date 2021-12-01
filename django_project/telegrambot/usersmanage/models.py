from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь",
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID пользователя Телеграм")
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    username = models.CharField(max_length=255, verbose_name="Username Telegram")
    email = models.EmailField(max_length=255, verbose_name="Email", null=True)
    age = models.PositiveIntegerField(verbose_name="Age")
    commentary = models.TextField(max_length=300, verbose_name="About the user", null=True)
    photo = models.CharField(verbose_name="Фото file_id", max_length=200)

    def __str__(self):
        return f"№{self.id} ({self.telegram_id}) - {self.name}"
