from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    short_description = models.TextField(verbose_name='Краткое описание', blank=True)
    long_description = HTMLField(verbose_name='Подробное описание', blank=True)
    lat = models.FloatField(verbose_name='Координаты: широта')
    lng = models.FloatField(verbose_name='Координаты: долгота')

    def __str__(self):
        return self.title


def get_directory_path(instance, filename):
    return f'places/{instance.place}/{filename}'


class Image(models.Model):
    place = models.ForeignKey('Place', verbose_name='Место', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фото', upload_to=get_directory_path, default='')

    def preview(self):
        height = 200 if (self.image.height) > 200 else (self.image.height)
        width = self.image.width / self.image.height * 200 if self.image.height > 200 else self.image.width
        return format_html(f'<img src="{self.image.url}" width="{width}" height="{height}" />')

    def __str__(self):
        return f'{self.pk} {self.place}'

    class Meta:
        ordering = ['-place', '-pk']