from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Юзер'
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='День рождения'
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        verbose_name='Фото'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
