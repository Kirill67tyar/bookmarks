from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as U

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


class Contact(models.Model):
    from_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
        verbose_name='Подписка от'
    )
    to_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='from_subscribed',
        verbose_name='Подписка на'
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Промежуточная таблица - контакте'

    def __str__(self):
        return f'{self.from_user} following to {self.to_user}'


following_field = models.ManyToManyField(
    to='self',
    through=Contact,
    related_name='followers',
    symmetrical=False,
    verbose_name='Подписан на'
)

# Динамическое добавление поля к модели (лучше не злоупотреблять)
# U.add_to_class('following', following_field)
User.add_to_class('following', following_field)
