from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from content_editor.models import create_plugin_base

from feincms3 import plugins as feincms3_plugins
from feincms3.mixins import TemplateMixin, LanguageMixin
from feincms3_meta.models import MetaMixin
from cms.utils import get_template_list
from cms import plugins
from feincms3.apps import reverse_app
from imagefield.fields import ImageField
from blog import plugins as article_plugins
from events import plugins as event_plugins
# Create your models here.


class Category(LanguageMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))

    image = ImageField(
        _("header image"), formats={
            'large': ['default', ('crop', (1920, 900))],
            'square': ['default', ('crop', (900, 900))],
            'card': ['default', ('crop', (900, 600))],
            'mobile': ['default', ('crop', (740, 600))],
            'preview': ['default', ('crop'), (1200, 600)],
        }, auto_add_fields=True, blank=True, null=True
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Namespace(LanguageMixin):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} ({self.language_code})"

    class Meta:
        verbose_name = _("name space")
        verbose_name_plural = _("name spaces")
        ordering = ['slug']


class Article(LanguageMixin, TemplateMixin, MetaMixin):
    TEMPLATES = get_template_list('blog', (
        (
            'default', ('main',)
        ),
    ))

    namespace = models.ForeignKey(
        Namespace, models.PROTECT,
        verbose_name=_("namespace")
    )

    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField(verbose_name=_("slug"), max_length=180)

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name=_("publication date")
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )

    edited_date = models.DateTimeField(
        auto_now=True, verbose_name=_("edited at")
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

    category = models.ForeignKey(
        Category, models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("category")
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_app(
            (f'blog-{self.namespace.slug}',),
            'article-detail',
            kwargs={
                'slug': self.slug
            },
            languages=[
                self.language_code
            ]
        )

    class Meta:
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'


PluginBase = create_plugin_base(Article)


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


class EventPlugin(event_plugins.EventPlugin, PluginBase):
    pass


class ArticlePlugin(article_plugins.ArticlePlugin, PluginBase):
    pass
