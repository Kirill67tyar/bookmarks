from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from images.utils import from_cyrilic_to_eng

User = get_user_model()


class Image(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='images_created',
        verbose_name='Владелец'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        verbose_name='Slug'
    )
    url = models.URLField(verbose_name='URL')

    image = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        verbose_name='Картинка'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )
    users_like = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='images_liked',
        verbose_name='Понравились пользователям'
    )
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(from_cyrilic_to_eng(str(self.title)))
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy(
            'images:detail',
            kwargs={
                'pk': self.pk,
                'slug': self.slug,
            }
        )
