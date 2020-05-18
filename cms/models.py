from content_editor.models import create_plugin_base
from django.db import models
from feincms3 import plugins as feincms3_plugins

from django.utils.translation import gettext_lazy as _
from feincms3.apps import AppsMixin
from feincms3.mixins import MenuMixin, RedirectMixin, TemplateMixin, LanguageMixin

from feincms3_meta.models import MetaMixin
from cms.utils import get_template_list
from cms import plugins
from blog import plugins as blog_plugins
from events import plugins as events_plugins

from feincms3_sites.middleware import current_site
from feincms3_sites.models import AbstractPage

from imagefield.fields import ImageField
# Create your models here.


class Page(
    AppsMixin,
    MetaMixin,
    TemplateMixin,
    RedirectMixin,
    MenuMixin,
    AbstractPage,
    LanguageMixin,
):
    APPLICATIONS = [
        (
            'blog',
            _("blog"),
            {
                'urlconf': 'blog.urls',
                'app_instance_namespace': lambda page: '-'.join(
                    ['blog', page.namespace.slug]
                )
            }
        ),
        (
            'events',
            _("events"),
            {
                'urlconf': 'events.urls',
                'app_instance_namespace': lambda page: '-'.join(
                    ['events']
                )
            }
        ),
        (
            'collection',
            _("collection"),
            {
                'urlconf': "link_collections.urls",
                "required_fields": ['collection'],
                'app_instance_namespace': lambda page: str(
                    page.slug
                ) + '-collections'
            }
        )
    ]

    MENUS = (
        ('main', _("main")),
        ('footer', _("footer")),
        ('featured', _("featured")),
    )

    TEMPLATES = get_template_list('cms', (
        (
            'default', ('main', 'footer')
        ),
    ))

    namespace = models.ForeignKey(
        'blog.Namespace', models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("namespace")
    )

    collection = models.ForeignKey(
        "link_collections.Collection", models.CASCADE, blank=True,
        null=True, verbose_name=_("collection")
    )

    image = ImageField(
        _("featured image"),
        upload_to='cms/',
        formats={
            'large': ['default', ('crop', (1920, 900))],
            'square': ['default', ('crop', (1024, 1024))],
            'preview': ['default', ('crop'), (1200, 600)],
        },
        auto_add_fields=True, blank=True, null=True,
    )

    def get_absolute_url(self, *args, **kwargs):
        site = current_site()
        if site == self.site:
            return super().get_absolute_url(*args, **kwargs)
        return '//' + self.site.host + super().get_absolute_url()

    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("page")
        ordering = ['position']


PluginBase = create_plugin_base(Page)


class External(feincms3_plugins.external.External, PluginBase):
    class Meta:
        verbose_name = _("external")


class RichText(feincms3_plugins.richtext.RichText, PluginBase):
    class Meta:
        verbose_name = _("rich text")


class Image(feincms3_plugins.image.Image, PluginBase):
    caption = models.CharField(_("caption"), max_length=200, blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)
    fullwidth = models.BooleanField(_("full width"), default=False)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")


class HTML(feincms3_plugins.html.HTML, PluginBase):
    class Meta:
        verbose_name = _("HTML")
        verbose_name_plural = _("HTML")


class Button(plugins.Button, PluginBase):
    pass


class EventPlugin(events_plugins.EventPlugin, PluginBase):
    pass


class ArticlePlugin(blog_plugins.ArticlePlugin, PluginBase):
    pass
