from django.db import models

from django_project.telegrambot.usersmanage.models.user import User


class ViewedProfile(models.Model):
    viewer = models.ForeignKey(User, related_name='viewer', on_delete=models.CASCADE)
    profile = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'profile')
