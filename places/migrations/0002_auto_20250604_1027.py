import json
import os

from django.db import migrations


def get_places(apps, schema_editor):
    Place = apps.get_model('places', 'Place')
    directory = 'places/static/places/places'
    file_names = [_ for _ in os.listdir(directory) if _.endswith('.json')]
    places = Place.objects.all()
    for name in file_names:
        with open(f'places/static/places/places/{name}', 'r', encoding='utf-8') as file:
            new_place = json.load(file)
        if new_place['title'] not in places.values_list('title', flat=True).distinct():
            Place.objects.get_or_create(title=new_place['title'], description_short=new_place['description_short'],
                                 description_long=new_place['description_long'], lat=new_place['coordinates']['lat'],
                                 lng=new_place['coordinates']['lng'])


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(get_places),
    ]