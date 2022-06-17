import requests
from urllib import request

from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from images.models import Image
from images.utils import from_cyrilic_to_eng


def get_extension(url: str) -> str:
    return url.split('.')[-1]


def check_extension(url):
    if not url.lower().endswith(('.jpg',
                                 '.jpeg',
                                 '.png',)):
        raise forms.ValidationError('The given url doest not match valid image extensions (jpg, jpeg, png)')
    return url


class ImageCreateModelForm(forms.ModelForm):
    # url = forms.URLField(widget=forms.HiddenInput, validators=[check_extension,])
    class Meta:
        model = Image
        fields = 'title', 'url', 'description',
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            if not url.lower().endswith(('.jpg',
                                         '.jpeg',
                                         '.png',)):
                raise forms.ValidationError('The given url does not match valid image extensions (jpg, jpeg, png)')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image_instance = super(ImageCreateModelForm, self).save(commit=False)
        cd = self.cleaned_data
        slug = slugify(from_cyrilic_to_eng(str(image_instance.title)))
        url = cd["url"]
        title_image = f'{slug}.{get_extension(url)}'
        # response = request.urlopen(url=url) # request  из urllib не работает
        response = requests.get(url=url)
        image_instance.image.save(
            name=title_image,
            content=ContentFile(response.content),
            save=False
        )
        if commit:
            image_instance.save()
        return image_instance

# content=ContentFile(response.read()),
# request из urllib не работает
# причина - https://stackoverflow.com/questions/16627227/problem-http-error-403-in-python-3-web-scraping

#                                          ContentFile
# https://docs.djangoproject.com/en/4.0/ref/files/file/#the-contentfile-class
# ContentFile - работает со строками, но может работать и с байтами
# ContentFile(response.content) - <ContentFile: Raw content>
# type(ContentFile(response.content)) - <class 'django.core.files.base.ContentFile'>
# dir(ContentFile(response.content)):
# chunks
# close
# closed
# encoding
# file
# fileno
# flush
# isatty
# multiple_chunks
# name
# newlines
# open
# read
# readable
# readinto
# readline
# readlines
# seek
# seekable
# size
# tell
# truncate
# writable
# write
# writelines
# кажется он преобразует строки и байты в тип данных похожий на встроенный
# тип данных Python для работы с файлами (FileObject или как то так)
