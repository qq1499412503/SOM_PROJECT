from djongo import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_profile = models.CharField(max_length=200)

    class Meta:
        pass


