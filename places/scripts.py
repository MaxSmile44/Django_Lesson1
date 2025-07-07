import requests

import json
import os

from django.core.files.base import ContentFile
from pathlib import Path
from places.models import *


def get_images():
    places = Place.objects.all()
    images = Image.objects.all()
    directory = 'places/static/places/places'
    file_names = [_ for _ in os.listdir(directory) if _.endswith('.json')]
    for name in file_names:
        with open(f'places/static/places/places/{name}', 'r', encoding='utf-8') as file:
            new_img = json.load(file)
        for i, link in enumerate(new_img['imgs'], 1):
            url = link
            directory = Path(f"./media/places/{new_img['title']}")
            if not directory.exists():
                directory.mkdir(parents=True)
            response = requests.get(url)
            response.raise_for_status()
            file_name = url.split('/')[-1]
            file_names = [_ for _ in os.listdir(directory)]
            if file_name not in file_names:
                images.create(place=places.get(title=new_img['title']),
                              image=ContentFile(response.content, name=file_name))


def get_places():
    places = Place.objects.all()
    directory = 'places/static/places/places'
    file_names = [_ for _ in os.listdir(directory) if _.endswith('.json')]
    for name in file_names:
        with open(f'places/static/places/places/{name}', 'r', encoding='utf-8') as file:
            new_place = json.load(file)
        if new_place['title'] not in places.values_list('title', flat=True).distinct():
            places.create(title=new_place['title'], slug=os.path.splitext(name)[0], description_short=new_place['description_short'],
                                 description_long=new_place['description_long'], lat=new_place['coordinates']['lat'],
                                 lng=new_place['coordinates']['lng'])