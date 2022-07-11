import csv
from django.http import HttpResponse

from .models import User


def export_users_csv(request):
    response = HttpResponse(content_type="text/csv")

    writer = csv.writer(response)
    writer.writerow([
        "id",
        "telegram_id",
        "name",
        "username",
        "sex",
        "age",
        "city",
        "need_city",
        "longitude",
        "latitude",
        "verification",
        "language",
        "varname",
        "lifestyle",
        "is_banned",
        "photo_id",
        "commentary",
        "need_partner_sex",
        "need_partner_age_min",
        "need_partner_age_max",
        "phone_number",
        "status",
        "instagram"
    ])
    for user in User.objects.all().values_list("id",
                                               "telegram_id",
                                               "name",
                                               "username",
                                               "sex",
                                               "age",
                                               "city",
                                               "need_city",
                                               "longitude",
                                               "latitude",
                                               "verification",
                                               "language",
                                               "varname",
                                               "lifestyle",
                                               "is_banned",
                                               "photo_id",
                                               "commentary",
                                               "need_partner_sex",
                                               "need_partner_age_min",
                                               "need_partner_age_max",
                                               "phone_number",
                                               "status",
                                               "instagram"):
        writer.writerow(user)

    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    return response
