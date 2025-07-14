import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from pathlib import Path

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Load places from json file'

    def add_arguments(self, parser):
        parser.add_argument('link', type=str, help='Link to json file')

    def handle(self, *args, **options):
        link = options['link']
        try:
            places = Place.objects.all()
            response = requests.get(link)
            response.raise_for_status()
            new_object = response.json()
            if new_object['title'] not in places.values_list('title', flat=True).distinct():
                images = Image.objects.all()
                places.create(title=new_object['title'],
                              short_description=new_object['description_short'],
                              long_description=new_object['description_long'], lat=new_object['coordinates']['lat'],
                              lng=new_object['coordinates']['lng'])

                directory = Path(f"./media/places/{new_object['title']}")
                if not directory.exists():
                    directory.mkdir(parents=True)
                for link in new_object['imgs']:
                    response = requests.get(link)
                    response.raise_for_status()
                    image_name = link.split('/')[-1]
                    images.create(place=places.get(title=new_object['title']),
                                  image=ContentFile(response.content, name=image_name))
                self.stdout.write(f'Successfully load file from link: {new_object["title"]}')
            else:
                self.stdout.write(f'This place has already been added earlier')
        except requests.exceptions.HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except NameError as error:
            print(f'Name error occurred: {error}')