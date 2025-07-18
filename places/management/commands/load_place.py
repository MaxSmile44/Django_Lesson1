import requests
import sys

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from places.models import Place, Image


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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
            places = Place.objects.prefetch_related('images').all()
            place, place_created = places.get_or_create(
                title=new_object['title'],
                defaults={
                    'short_description': new_object['description_short'],
                    'long_description': new_object['description_long'],
                    'lat': new_object['coordinates']['lat'],
                    'lng': new_object['coordinates']['lng']
                }
            )
            if place_created:
                self.stdout.write(f'Successfully load place from link: {new_object["title"]}')
            else:
                self.stdout.write(f'This place has already been added earlier')

            for number, link in enumerate(new_object['imgs'], 1):
                response = requests.get(link)
                response.raise_for_status()
                image_name = link.split('/')[-1]
                image, image_created = Image.objects.get_or_create(
                    place=get_object_or_404(places, title=new_object['title']),
                    number = number,
                    defaults={'image': ContentFile(response.content, name=image_name)}
                )
                if image_created:
                    self.stdout.write(f'Successfully load image {image_name} from link: {link}')
                else:
                    self.stdout.write(f'Image {image_name} has already been added earlier')

        except requests.exceptions.HTTPError as error:
            eprint(f'HTTP error occurred: {error}')
        except NameError as error:
            eprint(f'Name error occurred: {error}')