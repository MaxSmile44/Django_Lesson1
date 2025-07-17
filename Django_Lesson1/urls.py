from django.contrib import admin
from django.http import HttpResponseNotFound
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('places.urls')),
    path('tinymce/', include('tinymce.urls')),
] + debug_toolbar_urls()


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