import os

from asgiref.sync import sync_to_async

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "django_project.telegrambot.telegrambot.settings"
)
import django

django.setup()
from django.db.models import (
    F,
    Q,
)
from django.db.models.expressions import CombinedExpression, Value

from django_project.telegrambot.usersmanage.models import (
    UserMeetings,
    SettingModel,
    ViewedProfile,
    User,
    NecessaryLink,
)


@sync_to_async
def select_all_links():
    links = NecessaryLink.objects.all().values()
    return links


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.get(telegram_id=telegram_id)
    return user


@sync_to_async
def select_user_object(telegram_id: int):
    user = User.objects.get(telegram_id=telegram_id)
    return user


@sync_to_async
def add_profile_to_viewed(user, viewed_profile):
    return ViewedProfile.objects.create(viewer=user, profile=viewed_profile)


@sync_to_async
def check_user_exists(telegram_id: int):
    user_exists = User.objects.filter(telegram_id=telegram_id).exists()
    return user_exists


@sync_to_async
def check_user_meetings_exists(telegram_id: int):
    user_exists = UserMeetings.objects.filter(telegram_id=telegram_id).exists()
    return user_exists


@sync_to_async
def add_user(telegram_id, name, username, referrer_id=None):
    if referrer_id:
        return User(
            telegram_id=int(telegram_id),
            name=name,
            username=username,
            referrer_id=referrer_id,
        ).save()
    else:
        return User(telegram_id=int(telegram_id), name=name, username=username).save()


@sync_to_async
def delete_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).delete()


@sync_to_async
def delete_user_meetings(telegram_id):
    return UserMeetings.objects.filter(telegram_id=telegram_id).delete()


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


# https://stackoverflow.com/questions/29014966/django-1-8-arrayfield-append-extend
@sync_to_async
def update_user_events(telegram_id: int, events_id: int):
    return User.objects.filter(telegram_id=telegram_id).update(
        events=CombinedExpression(F("events"), "||", Value([f"{events_id}"]))
    )


@sync_to_async
def remove_events_from_user(telegram_id: int, events_id: int):
    user = User.objects.get(telegram_id=telegram_id)
    user.remove_events(f"{events_id}")


@sync_to_async
def select_user_username(username: str):
    user = User.objects.get(username=username)
    return user


# https://stackoverflow.com/questions/10040143/and-dont-work-with-filter-in-django
@sync_to_async
def search_users(
        need_partner_sex,
        need_age_min,
        need_age_max,
        user_need_city,
        offset: int,
        limit: int,
):
    query = (
            Q(is_banned=False)
            & Q(sex=need_partner_sex)
            & (
                    (Q(age__gte=need_age_min) & Q(age__lte=need_age_max))
                    | (Q(age__gte=need_age_min + 1) & Q(age__lte=need_age_max + 1))
            )
            & Q(city=user_need_city)
            & Q(status=True)
    )
    users = User.objects.filter(query).values()[offset: offset + limit]
    return users


@sync_to_async
def search_event_forms():
    return UserMeetings.objects.filter(Q(is_active=True)).all().values()


@sync_to_async
def search_users_all(offset: int, limit: int):
    return (
        User.objects.filter(Q(is_banned=False) & Q(status=True))
        .all()
        .values()[offset: offset + limit]
    )


@sync_to_async
def count_all_users_kwarg(**kwarg):
    return User.objects.filter(**kwarg).all().values().count()


@sync_to_async
def update_setting(telegram_id: int, **kwargs):
    return SettingModel.objects.filter(telegram_id=telegram_id).update(**kwargs)


@sync_to_async
def select_setting(telegram_id):
    return SettingModel.objects.get(telegram_id=telegram_id)


@sync_to_async
def add_user_to_settings(telegram_id: int):
    return SettingModel(telegram_id=int(telegram_id)).save()


@sync_to_async
def select_setting_tech_work():
    return SettingModel.objects.filter(technical_works=True).values().first()


@sync_to_async
def check_returned_event_id(telegram_id: int, id_of_events_seen: int) -> bool:
    """
    Функция, проверяющая, был ли ранее возвращен данный event_id для данного telegram_id
    """
    returned_event = User.objects.filter(telegram_id=telegram_id).first()
    event_list = returned_event.id_of_events_seen

    return str(id_of_events_seen) in event_list


@sync_to_async
def add_returned_event_id(telegram_id: int, id_of_events_seen: int):
    """
    Функция, добавляющая возвращенный event_id для данного telegram_id в базу данных
    """
    returned_event, created = User.objects.get_or_create(telegram_id=telegram_id)
    returned_event.id_of_events_seen.append(id_of_events_seen)
    returned_event.save()


@sync_to_async
def reset_view_limit():
    return User.objects.filter(limit_of_views__lt=10).update(limit_of_views=10)
