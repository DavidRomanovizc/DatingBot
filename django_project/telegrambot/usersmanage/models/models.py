from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_project.telegrambot.common.mixins import DateMixin

class Gender(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(models.Model):
    telegram_id = models.PositiveBigIntegerField(unique=True, default=1, verbose_name="Telegram User ID")
    name = models.CharField(max_length=255, verbose_name="User Name")
    username = models.CharField(max_length=255, verbose_name="Telegram Username")
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.BigIntegerField(verbose_name="Seeker's Age", null=True, blank=True)
    verification = models.BooleanField(verbose_name="Verification", default=False)
    language = models.CharField(max_length=10, verbose_name="User's Language", null=True, blank=True)
    varname = models.CharField(max_length=100, verbose_name="Public User Name", null=True, blank=True)
    is_banned = models.BooleanField(verbose_name="Is User Banned", default=False)
    phone_number = models.BigIntegerField(verbose_name="Phone Number", null=True, blank=True)
    status = models.BooleanField(verbose_name="Profile Status", default=False)
    instagram = models.CharField(max_length=200, verbose_name="Instagram Username", null=True, blank=True)

    def __str__(self):
        return f"#{self.id} ({self.telegram_id}) - {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    longitude = models.FloatField(verbose_name="User's Coordinates (longitude)", null=True, blank=True)
    latitude = models.FloatField(verbose_name="User's Coordinates (latitude)", null=True, blank=True)
    lifestyle = models.CharField(max_length=100, verbose_name="User's Lifestyle", null=True, blank=True)
    photo_id = models.CharField(max_length=400, verbose_name="Photo_ID", null=True)
    commentary = models.CharField(max_length=300, verbose_name="User's Comment", null=True, blank=True)
    need_partner_sex = models.CharField(max_length=50, verbose_name="Partner's Gender", null=True, blank=True)
    need_partner_age_min = models.PositiveIntegerField(verbose_name="Minimum Partner Age", default=18)
    need_partner_age_max = models.PositiveIntegerField(verbose_name="Maximum Partner Age", default=24)
    events = ArrayField(models.CharField(max_length=200), default=list)
    id_of_events_seen = ArrayField(models.CharField(max_length=255), default=list)

class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name="Event Name")
    time_event = models.CharField(max_length=10, verbose_name="Event Time", null=True)
    venue = models.CharField(max_length=50, verbose_name="Event Venue", null=True)
    need_location = models.CharField(max_length=50, null=True)
    verification_status = models.BooleanField(verbose_name="User Status", default=False)
    moderation_process = models.BooleanField(verbose_name="Moderation Process", default=True)
    is_premium = models.BooleanField(verbose_name="Premium", default=False)
    photo_id = models.CharField(max_length=400, verbose_name="Photo_ID", null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserMeeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    commentary = models.CharField(max_length=50, verbose_name="Comment", null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"#{self.id} ({self.user.telegram_id} - {self.user.username})"

class SettingModel(models.Model):
    telegram_id = models.PositiveBigIntegerField(unique=True, default=1, verbose_name="Telegram User ID")
    technical_works = models.BooleanField(default=False, verbose_name="Technical Works")
objects = models.Manager()
