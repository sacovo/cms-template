from content_editor.admin import ContentEditor
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3_meta.models import MetaMixin
from js_asset import JS

from blog import plugins as blog_plugins
from blog import models
from cms.plugins import ButtonInline
from events import plugins as event_plugins

# Register your models here.


@admin.register(models.Article)
class ArticleAdmin(ContentEditor):

    list_display = [
        'title',
        'slug',
        'publication_date',
        'category',
        'language_code',
        'namespace',
    ]

    list_filter = [
        'category',
        'namespace',
        'language_code',
    ]

    list_editable = [
        'language_code',
        'slug',
    ]

    date_hierarchy = 'publication_date'

    autocomplete_fields = [
        'category',
        'namespace',
    ]

    search_fields = [
        'title',
        'blog_richtext_set__text',
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = (
        'created_date',
        'edited_date',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'category',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'language_code',
                'slug',
                ('publication_date', 'created_date', 'edited_date'),
                'namespace',
                'template_key',
                'image',
                'image_ppoi'
            )
        }),
        MetaMixin.admin_fieldset(),
    )

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        ButtonInline.create(models.Button),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
        event_plugins.EventPluginInline.create(models.EventPlugin),
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


@admin.register(models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    list_display = [
        'name',
        'slug',
        'language_code',
    ]

    list_filter = [
        'language_code'
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'language_code')
        }),
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]

    list_display = [
        'name',
        'slug',
        'language_code',
    ]

    list_filter = [
        'language_code'
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'language_code')
        }),
    )
