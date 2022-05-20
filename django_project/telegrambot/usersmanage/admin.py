from django.contrib import admin

from .models import User, UserMeetings


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "username", "created_at")


@admin.register(UserMeetings)
class UserMeetingsAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "username", "created_at")