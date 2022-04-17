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
    sex = models.CharField(max_length=30, verbose_name="Пол искателя", null=True)
    age = models.BigIntegerField(verbose_name="Возраст искателя", default=18)
    city = models.CharField(max_length=40, verbose_name="Город искателя", null=True)
    verification = models.BooleanField(verbose_name="Верификация", default=False)
    language = models.CharField(max_length=10, verbose_name="Язык пользователя", null=True)
    varname = models.CharField(max_length=100, verbose_name="Публичное имя пользователя", null=True)
    lifestyle = models.CharField(max_length=100, verbose_name="Стиль жизни пользователя", null=True)
    is_banned = models.BooleanField(verbose_name="Забанен ли пользователь", default=False)
    photo_id = models.CharField(max_length=400, verbose_name="Photo_ID", null=True)
    commentary = models.CharField(max_length=300, verbose_name="Комментарий пользователя", null=True)
    need_partner_sex = models.CharField(max_length=50, verbose_name="Пол цели", null=True)
    likes = models.BigIntegerField(verbose_name="Количество лайков у пользователя", default=0)
    dislikes = models.BigIntegerField(verbose_name="Количество дизлайков у пользователя", default=0)
    phone_number = models.BigIntegerField(verbose_name="Номер телефона", null=True)

    def __str__(self):
        return f"№{self.id} ({self.telegram_id}) - {self.name}"
