from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


class ArticlePlugin(models.Model):
    articles = models.ManyToManyField(
        "blog.Article", related_name='%(app_label)s_%(class)s',
        verbose_name=_("articles"), blank=True,
    )

    title = models.CharField(_("title"), blank=True, max_length=180)

    count = models.IntegerField(_("count"), default=3)

    namespace = models.ForeignKey(
        "blog.NameSpace", models.SET_NULL, related_name='+',
        verbose_name=_("namespace"), blank=True, null=True,
    )

    template_key = models.CharField(
        max_length=100, default='blog/plugin_default.html',
        choices=settings.BLOG_TEMPLATE_CHOICES,
    )

    category = models.ForeignKey(
        "blog.Category", models.SET_NULL, related_name='+',
        verbose_name=_("category"), blank=True, null=True,
    )

    class Meta:
        abstract = True
        verbose_name = _("article plugin")
        verbose_name_plural = _("article plugins")

    def __str__(self):
        return self.title or _("articles")


class ArticlePluginInline(ContentEditorInline):
    autocomplete_fields = [
        'articles', 'category',
        'namespace',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'count',
                'category',
                'namespace',
                'ordering',
                'region'
            )
        }),
        (_("advanced"), {
            'classes': ('collapse',),
            'fields': (
                'articles',
                'template_key',
            )
        })
    )


def get_article_list(plugin):
    if plugin.articles.exists():
        return plugin.articles.all()
    from blog.models import Article

    articles = Article.objects.filter(
        language_code=plugin.parent.language_code,
    )

    if plugin.category:
        articles = articles.filter(category=plugin.category)

    if plugin.namespace:
        articles = articles.filter(namespace=plugin.namespace)

    return articles[:plugin.count]


def render_articles(plugin, **kwargs):
    return render_to_string(
        plugin.template_key, {
            'article_list': get_article_list(plugin),
            'plugin': plugin,
        }
    )
