from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telegram_chat_id = models.CharField(verbose_name="Чат ИД телеграм",
                                        max_length=200,
                                        blank=True, null=True)
    auth_token = models.CharField(verbose_name="Токен полученный с Телеграм",
                                        max_length=200,
                                        blank=True, null=True)