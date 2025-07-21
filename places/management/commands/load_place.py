import requests
import sys
import time

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

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
            place, place_created = Place.objects.prefetch_related('images').get_or_create(
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

            added_images_count = 0
            connection_attempts_number = 0
            images_count = len(new_object['imgs'])
            initial_number = 1
            while added_images_count < images_count:
                try:
                    for number, link in enumerate(new_object['imgs'], initial_number):
                        response = requests.get(link)
                        response.raise_for_status()
                        image_name = link.split('/')[-1]
                        image, image_created = Image.objects.get_or_create(
                            place=place,
                            number = number,
                            defaults={'image': ContentFile(response.content, name=image_name)}
                        )
                        if image_created:
                            self.stdout.write(f'Successfully load image {image_name} from link: {link}')
                            added_images_count += 1
                            new_object['imgs'].remove(link)
                            initial_number += 1
                        else:
                            self.stdout.write(f'Image {image_name} has already been added earlier')
                            added_images_count += 1
                            new_object['imgs'].remove(link)
                            initial_number += 1

                except requests.exceptions.HTTPError as error:
                    eprint(f'HTTP error occurred: {error}')
                    added_images_count += 1
                    new_object['imgs'].remove(link)
                except requests.exceptions.ConnectionError as error:
                    eprint(f'Connection error occurred: {error}')
                    connection_attempts_number += 1
                    if connection_attempts_number >= 3:
                        added_images_count += 1
                        new_object['imgs'].remove(link)
                        connection_attempts_number = 0
                        self.stdout.write(f'Image from link: {link} was not added. Connection error')
                    time.sleep(5)
                except requests.exceptions.ChunkedEncodingError as error:
                    eprint(f'ChunkedEncodingError occurred: {error}')
                    connection_attempts_number += 1
                    if connection_attempts_number >= 3:
                        added_images_count += 1
                        new_object['imgs'].remove(link)
                        connection_attempts_number = 0
                        self.stdout.write(f'Image from link: {link} was not added. Connection error')
                    time.sleep(5)
                except requests.exceptions.ReadTimeout as error:
                    eprint(f'ReadTimeout occurred: {error}')
                    if connection_attempts_number >= 3:
                        added_images_count += 1
                        new_object['imgs'].remove(link)
                        connection_attempts_number = 0
                        self.stdout.write(f'Image from link: {link} was not added. Connection error')
                    time.sleep(5)

        except requests.exceptions.ConnectionError as error:
            eprint(f'Connection error occurred: {error}')
        except requests.exceptions.ChunkedEncodingError as error:
            eprint(f'ChunkedEncodingError occurred: {error}')
        except KeyError as error:
            eprint(f'KeyError occurred: {error}')
        except NameError as error:
            eprint(f'Name error occurred: {error}')