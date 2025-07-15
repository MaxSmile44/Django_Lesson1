import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Load places from json file'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str, help='Link to json file')

    def handle(self, *args, **options):
        link = options['link']
        try:
            response = requests.get(link)
            response.raise_for_status()
            new_object = response.json()
            if new_object['title'] not in Place.objects.values_list('title', flat=True).distinct():
                Place.objects.get_or_create(
                    title=new_object['title'],
                    short_description=new_object['description_short'],
                    long_description=new_object['description_long'],
                    lat=new_object['coordinates']['lat'],
                    lng=new_object['coordinates']['lng']
                )

                for link in new_object['imgs']:
                    response = requests.get(link)
                    response.raise_for_status()
                    image_name = link.split('/')[-1]
                    Image.objects.get_or_create(
                        place=get_object_or_404(Place, title=new_object['title']),
                        image=ContentFile(response.content, name=image_name)
                    )
                self.stdout.write(f'Successfully load file from link: {new_object["title"]}')
            else:
                self.stdout.write(f'This place has already been added earlier')
        except requests.exceptions.HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except NameError as error:
            print(f'Name error occurred: {error}')