from django.db import models


class TimeBasedModel(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
