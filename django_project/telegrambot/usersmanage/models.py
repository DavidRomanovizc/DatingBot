from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_project.telegrambot.common.mixins import DateMixin


class User(DateMixin):
    class Meta:
        verbose_name = "Пользователь Знакомств",
        verbose_name_plural = "Пользователи Знакомств"

    id = models.AutoField(primary_key=True)
    telegram_id = models.PositiveBigIntegerField(
        unique=True, default=1, verbose_name="ID пользователя Телеграм"
    )
    name = models.CharField(
        max_length=255, verbose_name="Имя пользователя"
    )
    username = models.CharField(
        max_length=255, verbose_name="Username Telegram"
    )
    sex = models.CharField(
        max_length=30, verbose_name="Пол искателя", null=True, blank=True
    )
    age = models.BigIntegerField(
        verbose_name="Возраст искателя", null=True, blank=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город искателя", null=True, blank=True
    )
    need_city = models.CharField(
        max_length=255, verbose_name="Город партнера", null=True, blank=True
    )
    need_distance = models.PositiveIntegerField(
        verbose_name="Расстояние между партнерами", null=True, blank=True
    )
    longitude = models.FloatField(
        verbose_name="координаты пользователя", null=True, blank=True
    )
    latitude = models.FloatField(
        verbose_name="координаты пользователя", null=True, blank=True
    )
    verification = models.BooleanField(
        verbose_name="Верификация", default=False
    )
    language = models.CharField(
        max_length=10, verbose_name="Язык пользователя", null=True, blank=True
    )
    varname = models.CharField(
        max_length=100, verbose_name="Публичное имя пользователя", null=True, blank=True
    )
    lifestyle = models.CharField(
        max_length=100, verbose_name="Стиль жизни пользователя", null=True, blank=True
    )
    is_banned = models.BooleanField(
        verbose_name="Забанен ли пользователь", default=False
    )
    photo_id = models.CharField(
        max_length=400, verbose_name="Photo_ID", null=True
    )
    commentary = models.CharField(
        max_length=300, verbose_name="Комментарий пользователя", null=True, blank=True
    )
    need_partner_sex = models.CharField(
        max_length=50, verbose_name="Пол партнера", null=True, blank=True
    )
    need_partner_age_min = models.PositiveIntegerField(
        verbose_name="Минимальный возраст партнера", default=16
    )
    need_partner_age_max = models.PositiveIntegerField(
        verbose_name="Максимальный возраст партнера", default=24
    )
    referrer_id = models.PositiveBigIntegerField(
        verbose_name="реферал", null=True, blank=True
    )
    phone_number = models.BigIntegerField(
        verbose_name="Номер телефона", null=True, blank=True
    )
    status = models.BooleanField(
        verbose_name="Статус анкеты", default=False
    )
    instagram = models.CharField(
        max_length=200, verbose_name="Ник в инстаграме", null=True, blank=True
    )
    events = ArrayField(models.CharField(
        max_length=200), default=list
    )
    id_of_events_seen = ArrayField(
        models.CharField(max_length=255), default=list
    )

    def __str__(self):
        return f"№{self.id} ({self.telegram_id}) - {self.name}"

    def remove_events(self, event_to_remove):
        if event_to_remove in self.events:
            self.events.remove(event_to_remove)
            self.save()


class UserMeetings(DateMixin):
    class Meta:
        verbose_name = "Пользователь Мероприятий",
        verbose_name_plural = "Пользователи Мероприятий"

    id = models.AutoField(primary_key=True)
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


class SettingModel(DateMixin):
    telegram_id = models.PositiveBigIntegerField(
        unique=True, default=1, verbose_name="ID пользователя Телеграм"
    )
    technical_works = models.BooleanField(
        default=False, verbose_name="Технические работы"
    )

    objects = models.Manager()
