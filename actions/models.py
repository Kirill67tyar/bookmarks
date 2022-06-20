from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Action(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='actions',
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='Юзер'
    )
    verb = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    target_ct = models.ForeignKey(
        to=ContentType,
        related_name='target_obj',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    target_id = models.PositiveIntegerField(
        blank=True, null=True,
        db_index=True,
    )
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Создано'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'

    def __str__(self):
        return f'{self.user} {self.verb} - {self.created}'
