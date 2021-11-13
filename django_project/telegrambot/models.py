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
    LIFESTYLES = [
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
    user_var_name = models.CharField(verbose_name='Произвольное имя пользователя')
    lifestyle = models.CharField(verbose_name='Стиль жизни пользователя', choices=LIFESTYLES)
    is_banned = models.BooleanField(verbose_name='Наличие бана у пользователя')
    photo_id = models.CharField(verbose_name='Photo ID пользователя')
    commentary = models.CharField(verbose_name='Комментарий к анкете', max_length=255)
    likes = models.BigIntegerField(verbose_name='Лайки пользователя')
    dislikes = models.BigIntegerField(verbose_name='Дизлайки пользователя')
    registration_complete = models.BooleanField(verbose_name='Пройдена ли регистрация')

    def __str__(self):
        return f'№{self.id} - {self.telegram_id} - {self.username} - {self.full_name}'


class Purchase(TimeBasedModel):
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET(0))
    amount = models.DecimalField(verbose_name='Стоимость покупки', decimal_places=2, max_digits=8)
    purchase_time = models.DateTimeField(verbose_name='Время покупки', auto_now_add=True)

    def __str__(self):
        return f'№{self.id} - {self.buyer} - {self.amount} - {self.purchase_time}'


class Referral(TimeBasedModel):
    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Рефералы'

    id = models.ForeignKey(User, unique=True, primary_key=True, on_delete=models.CASCADE)
    referrer_id = models.BigIntegerField()
    referrer_username = models.CharField(max_length=255, verbose_name='Пригласитель', default=None)

    def __str__(self):
        return f'№{self.id} - от {self.referrer_id} / {self.referrer_username}'
