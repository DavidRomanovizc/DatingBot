from django.db import (
    models,
)

from django_project.telegrambot.usersmanage.models.base import (
    TimeBasedModel,
)


class SettingModel(TimeBasedModel):
    telegram_id = models.PositiveBigIntegerField(
        unique=True, default=1, verbose_name="ID пользователя Телеграм"
    )
    technical_works = models.BooleanField(
        default=False, verbose_name="Технические работы"
    )

    objects = models.Manager()
