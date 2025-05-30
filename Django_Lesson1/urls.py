"""
URL configuration for Django_Lesson1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('map.urls')),
]


def bad_request_handler(request, exception):
    return HttpResponseNotFound("<h1>Невозможно обработать запрос</h1>")


def permission_denied_handler(request, exception):
    return HttpResponseNotFound("<h1>Доступ запрещен</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def server_error(request):
    return HttpResponseNotFound("<h1>Ошибка сервера</h1>")


handler400 = bad_request_handler
handler403 = permission_denied_handler
handler404 = page_not_found
handler500 = server_error