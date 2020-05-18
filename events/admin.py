from content_editor.admin import ContentEditor
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3_meta.models import MetaMixin
from geopy.geocoders import Nominatim
from js_asset import JS

from cms.plugins import ButtonInline
from events import models
from events import plugins as event_plugins
from blog import plugins as blog_plugins

# Register your models here.


@admin.register(models.Event)
class EventAdmin(ContentEditor):
    list_display = [
        'title',
        'slug',
        'start_date',
        'end_date',
        'location',
        'language_code',
    ]

    list_filter = [
        'language_code',
    ]

    search_fields = [
        'location',
        'title',
        'description',
    ]

    date_hierarchy = 'start_date'

    autocomplete_fields = [
        'location',
    ]

    search_fields = [
        'title',
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'author',
                ('start_date', 'end_date',),
                'location',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'language_code',
                'slug',
                'template_key',
                'header_image',
                'header_image_ppoi'
            )
        }),
        MetaMixin.admin_fieldset(),
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        event_plugins.EventPluginInline.create(models.EventPlugin),
        ButtonInline.create(models.Button),
    ]

    class Media:
        js = (
            'admin/js/jquery.init.js',
            JS('https://use.fontawesome.com/0fc4ca6dfe.js', {
                'async': 'async',
                'crossorigin': 'anonymous',
            }, static=False),
            'admin/plugin_buttons.js',
        )


@admin.register(models.Location)
class LocationAdmin(ContentEditor):
    search_fields = [
        'name',
        'street',
        'city',
    ]

    list_display = [
        'name',
        'slug',
        'street',
        'city',
        'lng',
        'lat',
    ]

    list_filter = [
        'city'
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'street',
                ('city', 'zip_code',),
                'country',
            )
        }),
        (_('advanced'), {
            'classes': ('tabbed',),
            'fields': (
                'slug',
                'lat',
                'lng',
                'header_image',
                'header_image_ppoi'
            )
        }),
        MetaMixin.admin_fieldset(),
    )

    inlines = [
        plugins.image.ImageInline.create(models.LocationImage),
    ]

    def save_model(self, request, obj, form, change):
        if(not change):
            locator = Nominatim(user_agent=settings.NOMINATIM_USER_AGENT)
            location = locator.geocode(
                f"{obj.street}, {obj.zip_code} {obj.city}, {obj.country}"
            )
            obj.lat = location.latitude
            obj.lng = location.longitude
        super().save_model(request, obj, form, change)
