from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin

from .models import *


class ImageInline(SortableStackedInline):
    model = Image
    readonly_fields = ['preview']
    fields = [('place', 'image'), 'preview']
    extra = 0


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ('title',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['place']