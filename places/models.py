from django.db import models
from django.utils.html import format_html
from pathlib import PurePath
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
    return PurePath('places', f"{instance.place}", f"{filename}")


class Image(models.Model):
    place = models.ForeignKey('Place', verbose_name='Место', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фото', upload_to=get_directory_path)
    number = models.PositiveIntegerField(verbose_name='Номер фото', default=0, null=False, blank=False)

    def preview(self):
        return format_html(
            '<img src="{}" style="max-width: 400px; max-height: 200px; width: auto; height: auto;" />',
            self.image.url
        )

    def __str__(self):
        return f'{self.number} {self.place}'

    class Meta:
        ordering = ['-place', '-number']
        indexes = [
            models.Index(fields=['number'])
        ]