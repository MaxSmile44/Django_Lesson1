from django.urls import path
from . import views
from .scripts import get_images, get_places


urlpatterns = [
    path('', views.index, name='home'),
]

get_places()
get_images()