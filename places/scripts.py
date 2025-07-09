import requests

import json
import os

from django.core.files.base import ContentFile
from pathlib import Path
from places.models import *


def add_place(places, new_object, name):
    places.create(title=new_object['title'], slug=os.path.splitext(name)[0],
                  description_short=new_object['description_short'],
                  description_long=new_object['description_long'], lat=new_object['coordinates']['lat'],
                  lng=new_object['coordinates']['lng'])


def add_image(places, images, new_object):
        for link in new_object['imgs']:
            directory = Path(f"./media/places/{new_object['title']}")
            if not directory.exists():
                directory.mkdir(parents=True)
            response = requests.get(link)
            response.raise_for_status()
            file_name = link.split('/')[-1]
            images.create(place=places.get(title=new_object['title']),
                          image=ContentFile(response.content, name=file_name))


def add_places_with_images():
    places = Place.objects.all()
    images = Image.objects.all()
    directory = 'places/static/places/files/'
    file_names = [_ for _ in os.listdir(directory) if _.endswith('.json')]
    for name in file_names:
        with open(f'{directory}{name}', 'r', encoding='utf-8') as file:
            new_object = json.load(file)
        if new_object['title'] not in places.values_list('title', flat=True).distinct():
            add_place(places, new_object, name)
            add_image(places, images, new_object)