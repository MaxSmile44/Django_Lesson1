from django.db import models

#from asgi import application


# Create your models here.
class Place(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Подробное описание')
    lat = models.FloatField(verbose_name='Координаты: широта')
    lng = models.FloatField(verbose_name='Координаты: долгота')

    def __str__(self):
        return self.title


def get_directory_path(instance, filename):
    return f'places/{instance.place}/{filename}'


class Image(models.Model):
    place = models.ForeignKey('Place', verbose_name='Место', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фото', upload_to=get_directory_path, null=True, blank=True)

    def __str__(self):
        return f'{self.pk} {self.place}'

    class Meta:
        ordering = ['-place', '-pk']