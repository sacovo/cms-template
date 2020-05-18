from django.contrib import admin
from content_editor.admin import ContentEditor
from django.utils.translation import gettext_lazy as _
from feincms3 import plugins
from feincms3.admin import TreeAdmin
from feincms3_meta.models import MetaMixin
from js_asset import JS

from cms import models
from cms.plugins import ButtonInline
from blog import plugins as blog_plugins
from events import plugins as events_plugins


@admin.register(models.Page)
class PageAdmin(ContentEditor, TreeAdmin):
    list_display = [
        "indented_title",
        "move_column",
        'slug',
        'static_path',
        'path',
        "is_active",
        'language_code',
        "template_key",
        'application',
        "position",
    ]
    actions = ['copy_selected']

    prepopulated_fields = {'slug': ('title',)}

    autocomplete_fields = [
        'parent',
        'namespace',
        'redirect_to_page',
        'collection',
    ]

    search_fields = ['title']

    list_editable = [
        'is_active',
        'slug',
        'static_path',
        'path',
        'language_code',
    ]

    list_filter = ['is_active', 'menu', 'language_code', 'site']

    inlines = [
        plugins.richtext.RichTextInline.create(models.RichText),
        plugins.image.ImageInline.create(models.Image),
        plugins.html.HTMLInline.create(models.HTML),
        plugins.external.ExternalInline.create(models.External),
        ButtonInline.create(models.Button),
        events_plugins.EventPluginInline.create(models.EventPlugin),
        blog_plugins.ArticlePluginInline.create(models.ArticlePlugin),
    ]

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'parent',
            )
        }),
        (_('settings'), {
            'classes': ('tabbed',),
            'fields': (
                'is_active',
                'menu',
                'language_code',
                'template_key',
                'image',
                'image_ppoi'
            ),
        }),
        (_('path'), {
            'classes': ('tabbed',),
            'fields': (
                'slug',
                'static_path',
                'path',
                'site',
            )
        }),
        (_('application'), {
            'classes': ('tabbed', ),
            'fields': (
                'application',
                'namespace',
                'collection',
            )
        }),
        MetaMixin.admin_fieldset(),
        (_('redirect'), {
            'classes': ('tabbed',),
            'fields': (
                'redirect_to_page',
                'redirect_to_url',
            )
        }),
    )

    mptt_level_indent = 30

    class Media:
        js = (
            'admin/js/jquery.init.js',
            JS('https://use.fontawesome.com/0fc4ca6dfe.js', {
                'async': 'async',
                'crossorigin': 'anonymous',
            }, static=False),
            'admin/plugin_buttons.js',
        )
