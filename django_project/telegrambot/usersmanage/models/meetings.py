from django.db import models

from django_project.telegrambot.usersmanage.models.base import TimeBasedModel


class UserMeetings(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь Мероприятий",
        verbose_name_plural = "Пользователи Мероприятий"

    telegram_id = models.PositiveBigIntegerField(
        unique=True, default=1, verbose_name="ID пользователя Телеграм"
    )
    username = models.CharField(
        max_length=255, verbose_name="Username Telegram"
    )
    commentary = models.CharField(
        max_length=50, verbose_name="Комментарий", null=True
    )
    time_event = models.CharField(
        max_length=10, verbose_name="Время проведения", null=True
    )
    venue = models.CharField(
        max_length=50, verbose_name="Место проведения", null=True
    )
    need_location = models.CharField(
        max_length=50, null=True
    )
    event_name = models.CharField(
        max_length=50, verbose_name="Название мероприятия", null=True
    )
    verification_status = models.BooleanField(
        verbose_name="Статус пользователя", default=False
    )
    moderation_process = models.BooleanField(
        verbose_name="Процесс модерации", default=True
    )
    is_premium = models.BooleanField(
        verbose_name="Премиум", default=False
    )
    photo_id = models.CharField(
        max_length=400, verbose_name="Photo_ID", null=True
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"№{self.id} ({self.telegram_id} - {self.username})"

