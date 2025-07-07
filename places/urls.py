from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .scripts import add_to_db


urlpatterns = [
    path('', views.index, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

add_to_db()