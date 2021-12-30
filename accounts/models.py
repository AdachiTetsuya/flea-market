from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    class Meta:
        verbose_name_plural = 'CustomUser'

    icon = models.FileField(
        verbose_name="アイコン画像", upload_to="uploads/icon", default='default/people-24px.svg'
    )

    sell_num = models.IntegerField(
        default=0,
    )

    buy_num = models.IntegerField(
        default=0,
    )

    introduction = models.TextField(
        blank=True,
        null=True,
        max_length=5000,
    )

    