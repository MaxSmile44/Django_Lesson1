import requests

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place, Image


def index(request):
    places = Place.objects.all()
    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.title,
                'detailsUrl': requests.get(
                    request.build_absolute_uri(reverse('places', kwargs={'place_id': place.id}))
                ).json()
            }
        } for place in places
    ]
    context = {'value': {'type': 'FeatureCollection', 'features': features}}
    return render(request, 'places/index.html', context)


def places(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related(
        Prefetch('images', queryset=Image.objects.order_by('pk'))
    ), pk=place_id)
    imgs = [f'{settings.MEDIA_URL}{place_image.image}' for place_image in place.images.all()]
    place_details = {
        'title': place.title,
        'imgs': imgs,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {'lng': place.lng, 'lat': place.lat},
    }
    return JsonResponse(place_details, safe=True, json_dumps_params={'ensure_ascii': False, 'indent': 2})