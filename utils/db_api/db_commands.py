from asgiref.sync import sync_to_async
from django_project.telegrambot.usersmanage.models import User, UserMeetings


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).values().first()
    return user


@sync_to_async
def add_user(telegram_id, name, username):
    return User(telegram_id=int(telegram_id), name=name, username=username).save()


@sync_to_async
def delete_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).delete()


@sync_to_async
def add_meetings_user(telegram_id, username):
    return UserMeetings(telegram_id=int(telegram_id), username=username).save()


@sync_to_async
def select_all_user_meetings():
    users = UserMeetings.objects.all().values()
    return users


@sync_to_async
def select_user_meetings(telegram_id: int):
    user = UserMeetings.objects.filter(telegram_id=telegram_id).values().first()
    return user


@sync_to_async
def select_all_users():
    users = User.objects.all().values()
    return users


@sync_to_async
def select_all_users_id(telegram_id: int):
    users = User.objects.filter(telegram_id=telegram_id).all().values()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def update_user_data(telegram_id, **kwargs):
    return User.objects.filter(telegram_id=telegram_id).update(**kwargs)


@sync_to_async
def update_user_meetings_data(telegram_id, **kwargs):
    return UserMeetings.objects.filter(telegram_id=telegram_id).update(**kwargs)


@sync_to_async
def select_meetings_user(telegram_id: int):
    user = UserMeetings.objects.filter(telegram_id=telegram_id).values().first()
    return user


@sync_to_async
def select_user_username(username: str):
    user = User.objects.filter(username=username).values().first()
    return user


@sync_to_async
def search_user(need_partner_sex):
    return User.objects.filter(sex=need_partner_sex).all().values()
