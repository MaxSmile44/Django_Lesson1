from django.contrib import admin

from .models import *


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ('get_preview',)


@admin.register(Place)
class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['get_preview']