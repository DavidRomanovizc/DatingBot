from django.contrib import admin

from django_project.telegrambot.usersmanage.models.meetings import UserMeetings
from django_project.telegrambot.usersmanage.models.necessary_link import NecessaryLink
from django_project.telegrambot.usersmanage.models.settings_models import SettingModel
from django_project.telegrambot.usersmanage.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "username", "created_at")


@admin.register(UserMeetings)
class UserMeetingsAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "username", "created_at")


@admin.register(SettingModel)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "technical_works")


@admin.register(NecessaryLink)
class NecessaryLinkAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "link",
        "telegram_link_id",
        "title"
    ]

    search_fields = ("link__startswith", "title__startswith", "telegram_link_id__startswith")
