from django.contrib import (
    admin,
)
from django.urls import (
    path,
)

from django_project.telegrambot.usersmanage import (
    views,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("export/", views.export_users_csv),
]
