from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователей созданная для приложения foodgram"""

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        db_index=True,
        verbose_name='Email',
        help_text='Введите email'
    )

    username = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='Логин',
        help_text='Введите ваш логин'
    )

    first_name = models.TextField(
        verbose_name='Имя',
        blank=False,
        null=False,
        help_text='Введите имя'
    )
    second_name = models.TextField(
        verbose_name='Фамилия',
        blank=False,
        null=False,
        help_text='Введите фамилию'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
    def __str__(self):
        return self.username
