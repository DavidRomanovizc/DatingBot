from django.db import models

from django_project.telegrambot.usersmanage.models.base import TimeBasedModel


class NecessaryLink(TimeBasedModel):
    class Meta:
        verbose_name = "Необходимая ссылка"
        verbose_name_plural = "Необходимые ссылки"

    id = models.AutoField(primary_key=True)
    link = models.URLField(verbose_name="Обязательная ссылка")
    telegram_link_id = models.BigIntegerField(verbose_name="id КАНАЛА/ЧАТА - ОБЯЗАТЕЛЬНО")
    title = models.CharField(verbose_name="Название кнопки - ОБЯЗАТЕЛЬНО. Можно смайлики", max_length=50)
