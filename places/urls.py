from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .scripts import get_images, get_places


urlpatterns = [
    path('', views.index, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# get_places()
# get_images()