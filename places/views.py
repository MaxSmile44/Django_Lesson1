from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from places.models import Place, Image


def index(request):
    places = Place.objects.prefetch_related(
        Prefetch('images', queryset=Image.objects.order_by('pk'))
    )
    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': "Point",
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.title,
                'detailsUrl': {
                    'title': place.title,
                    'short_description': place.short_description,
                    'long_description': place.long_description,
                    'imgs': [
                        request.build_absolute_uri(place_image.image.url)
                        for place_image in place.images.all()
                    ],
                },
            }
        } for place in places
    ]
    context = {'value': {'type': 'FeatureCollection', 'features': features}}
    return render(request, 'places/index.html', context)


def places(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related(
        Prefetch('images', queryset=Image.objects.order_by('pk'))
    ), pk=place_id)
    imgs = [
        request.build_absolute_uri(place_image.image.url)
        for place_image in place.images.all()
    ]
    details = {
        'title': place.title,
        'imgs': imgs,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {'lng': place.lng, 'lat': place.lat},
    }
    return JsonResponse(details, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})



