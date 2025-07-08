from django.db.models import Prefetch
from django.shortcuts import render

from places.models import *


def index(request):
    places = Place.objects.prefetch_related(
        Prefetch('images', queryset=Image.objects.order_by('pk'))
    )
    context = {'value': {'type': 'FeatureCollection', 'features': []}}
    for place in places:
        imgs = list()
        for place_image in place.images.all():
            imgs.append(request.build_absolute_uri(place_image.image.url))
        detailsUrl = {
            'title': place.title,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'imgs': imgs,
        }
        features = {
            'type': 'Feature',
            'geometry': {
                'type': "Point",
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.slug,
                'detailsUrl': detailsUrl
            }
        }
        context['value']['features'].append(features)
    return render(request, 'places/index.html', context)