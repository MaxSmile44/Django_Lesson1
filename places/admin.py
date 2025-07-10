from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin

from .models import *


class ImageInline(SortableStackedInline):
    model = Image
    readonly_fields = ['get_preview']
    fields = [('place', 'image'), 'get_preview']
    extra = 0


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['get_preview']