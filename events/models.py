from django.db import models
from content_editor.models import Region, create_plugin_base

from django.utils import timezone
from cms.utils import get_template_list
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins as feincms3_plugins
from cms import plugins
from blog import plugins as blog_plugins
from events import plugins as event_plugins
from feincms3.apps import reverse_app
from feincms3_meta.models import MetaMixin
from feincms3.mixins import LanguageMixin, TemplateMixin

from imagefield.fields import ImageField


class Location(MetaMixin, LanguageMixin):
    regions = [Region(key='images', title=_("images"))]
    name = models.CharField(
        max_length=200, verbose_name=_("name")
    )
    slug = models.SlugField(
        unique=True
    )

    street = models.CharField(
        max_length=200, verbose_name=_("street")
    )
    city = models.CharField(
        max_length=100, verbose_name=_("city")
    )
    zip_code = models.CharField(
        max_length=20, verbose_name=_("zip code")
    )

    country = models.CharField(
        max_length=200, verbose_name=_("country")
    )

    image = ImageField(
        _("header image"), formats={
            'large': ['default', ('crop', (1920, 900))],
            'square': ['default', ('crop', (900, 900))],
            'card': ['default', ('crop', (900, 600))],
            'mobile': ['default', ('crop', (740, 600))],
            'preview': ['default', ('crop'), (1200, 600)],
        }, auto_add_fields=True, blank=True, null=True
    )

    website = models.URLField(blank=True, verbose_name=_("website"))

    lng = models.FloatField(verbose_name=_("longitude"), default=0)
    lat = models.FloatField(verbose_name=_("latitude"), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_app(
            ['events'],
            'location-detail',
            kwargs={
                'slug': self.slug
            }
        )


LocationPluginBase = create_plugin_base(Location)


class LocationImage(
    feincms3_plugins.image.Image, LocationPluginBase
):
    caption = models.CharField(
        _("caption"), max_length=200, blank=True
    )


class Event(MetaMixin, LanguageMixin, TemplateMixin):
    TEMPLATES = get_template_list('events', (
        (
            'default', ('main',),
        ),
    ))

    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField(verbose_name=_("slug"), max_length=180)

    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date")
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )

    edited_date = models.DateTimeField(
        auto_now=True, verbose_name=_("edited at")
    )

    location = models.ForeignKey(
        Location, models.SET_NULL,
        blank=True, null=True, verbose_name=_("location")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['start_date']
        indexes = [
            models.Index(fields=[
                'start_date', 'slug', 
            ])
        ]
        constraints = [
            models.UniqueConstraint(fields=[
                'slug', 'start_date', 
            ], name="unique_slugs_for_date")
        ]

    def get_absolute_url(self):
        return reverse_app(
            ['events'],
            'event-detail',
            kwargs={
                'slug': self.slug,
                'day': self.start_date.day,
                'month': self.start_date.month,
                'year': self.start_date.year,
            }
        )


PluginBase = create_plugin_base(Event)


class External(feincms3_plugins.external.External, PluginBase):
    pass


class RichText(feincms3_plugins.richtext.RichText, PluginBase):
    pass


class Image(feincms3_plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)
    fullwidth = models.BooleanField(_("full width"), default=False)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class HTML(feincms3_plugins.html.HTML, PluginBase):
    pass


class Button(plugins.Button, PluginBase):
    pass


class ArticlePlugin(blog_plugins.ArticlePlugin, PluginBase):
    pass


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass
