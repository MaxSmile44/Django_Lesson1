from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .scripts import add_places_with_images


urlpatterns = [
    path('', views.index, name='home'),
    path('places/<int:place_id>', views.places, name='places'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

add_places_with_images()