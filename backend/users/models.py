from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователей созданная для приложения foodgram"""

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
