from django.contrib import admin

from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'image', 'created',)
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('title',), }
