from django_project.telegrambot.usersmanage.models import User
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    return user


@sync_to_async
def add_user(telegram_id, name, username, age):
    return User(telegram_id=int(telegram_id), fullname=name, username=username, age=int(age)).save()


@sync_to_async
def select_all_users():
    users = User.objects.all()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()
