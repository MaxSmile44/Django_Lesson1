import requests

import json
import os

from django.core.files.base import ContentFile
from pathlib import Path
from places.models import *


def add_places(file_names, places, new_object, name):
    places.create(title=new_object['title'], slug=os.path.splitext(name)[0],
                  description_short=new_object['description_short'],
                  description_long=new_object['description_long'], lat=new_object['coordinates']['lat'],
                  lng=new_object['coordinates']['lng'])


def add_images(file_names, places, images, new_object):
        for i, link in enumerate(new_object['imgs'], 1):
            url = link
            directory = Path(f"./media/places/{new_object['title']}")
            if not directory.exists():
                directory.mkdir(parents=True)
            response = requests.get(url)
            response.raise_for_status()
            file_name = f"{i}{os.path.splitext(url.split('/')[-1])[1]}"
            file_names = [_ for _ in os.listdir(directory)]
            if file_name not in file_names:
                images.create(place=places.get(title=new_object['title']),
                              image=ContentFile(response.content, name=file_name))


def add_to_db():
    places = Place.objects.all()
    images = Image.objects.all()
    directory = 'places/static/places/places'
    file_names = [_ for _ in os.listdir(directory) if _.endswith('.json')]
    for name in file_names:
        with open(f'places/static/places/places/{name}', 'r', encoding='utf-8') as file:
            new_object = json.load(file)
        if new_object['title'] not in places.values_list('title', flat=True).distinct():
            add_places(file_names, places, new_object, name)
            add_images(file_names, places, images, new_object)