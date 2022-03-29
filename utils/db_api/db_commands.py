from django_project.telegrambot.usersmanage.models import User
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).values().first()
    return user


@sync_to_async
def add_user(telegram_id, name, username):
    return User(telegram_id=int(telegram_id), name=name, username=username).save()


@sync_to_async
def select_all_users():
    users = User.objects.all().values()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def update_user_data(telegram_id, **kwargs):
    return User.objects.filter(telegram_id=telegram_id).update(**kwargs)
