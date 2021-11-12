from django.db import models


# Create your models here.


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True, verbose_name='ID юзера телеграм')
    full_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    username = models.CharField(max_length=100, verbose_name='Юзернейм пользователя')
    email = models.CharField(max_length=100, verbose_name='Почта пользователя', null=True)
    SEX = [
        ('male', 'Мужской'),
        ('female', 'Женский')
    ]
    AGE_GROUPS = [
        ('up_to_25', 'До 25-ти'),
        ('25-45', '25-45'),
        ('after_45', '45+'),
    ]
    AGE_GROUPS_TARGET = [
        ('up_to_25', 'До 25-ти'),
        ('25-45', '25-45'),
        ('after_45', '45+'),
        ('same', 'Ровесники'),
    ]
    EDUCATION = [
        ('higher', 'Высшее'),
        ('secondary_edu', 'Среднее'),
    ]
    CITY_CHOICE = [
        ('my_city', 'В одном городе'),
        ('other_city', 'В другом городе'),
    ]
    LOCALE_GROUPS = [
        ('en', 'Англоговорящий'),
        ('ru', 'Русскоговорящий')
    ]

    sex = models.CharField(max_length=10, verbose_name='Пол пользователя', choices=SEX)
    sex_target = models.CharField(max_length=10, verbose_name='Цель поиска', choices=SEX)
    age = models.BigIntegerField(verbose_name='Возраст пользователя')
    age_group = models.BigIntegerField(verbose_name='Возрастная группа пользователя', choices=AGE_GROUPS)
    age_group_target = models.CharField(verbose_name='Целевая возрастная группа', choices=AGE_GROUPS_TARGET)
    national = models.CharField(verbose_name='Национальность пользователя', max_length=70)
    education = models.CharField(verbose_name='Образование пользователя', choices=EDUCATION)
    education_target = models.CharField(verbose_name='Образование целевого пользователя', choices=EDUCATION)
    city = models.CharField(verbose_name='Город пользователя')
    city_target = models.CharField(verbose_name='Город целевого пользователя', choices=CITY_CHOICE)
    kids = models.BooleanField(verbose_name='Наличие детей у пользователя', default=False)
    kids_target = models.BooleanField(verbose_name='Наличие детей у целевого пользователя', default=False)
    car = models.BooleanField(verbose_name='Наличие машины у пользователя', default=False)
    car_target = models.BooleanField(verbose_name='Наличие машины у целевого пользователя', default=False)
    apartment = models.BooleanField(verbose_name='Наличие жил.площади у пользователя', default=False)
    apartment_target = models.BooleanField(verbose_name='Наличие жил. площади у целевого пользователя', default=False)
    marital = models.BooleanField(verbose_name='Наличие партнера у пользователя', default=False)
    marital_target = models.BooleanField(verbose_name='Наличие партнера у целевого пользователя', default=False)
    locale = models.CharField(verbose_name='Язык пользователя', choices=LOCALE_GROUPS)
