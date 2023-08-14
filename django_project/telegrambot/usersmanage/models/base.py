from django.db import models


class TimeBasedModel(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления',
    )

    class Meta:
        abstract = True
