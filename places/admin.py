from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin

from .models import Place, Image


class ImageInline(SortableStackedInline):
    model = Image
    readonly_fields = ['preview']
    fields = [('place', 'image'), 'preview']
    extra = 0


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ('title',)
    list_display = ['title']
    list_filter = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['place']
    readonly_fields = ['preview']
    list_display = ['place', 'number', 'place', 'preview']
    list_filter = ['place']