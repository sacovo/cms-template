from django.utils.html import mark_safe
from feincms3.renderer import TemplatePluginRenderer

from feincms3 import plugins
from django.template.loader import render_to_string
from cms import models as pages
from blog import plugins as article_plugins
from events import plugins as events_plugins
from feincms3.plugins.external import oembed_html, oembed_json



def render_richtext(plugin):
    return render_to_string('plugins/text.html', {
        'content': plugins.richtext.render_richtext(plugin),
        'plugin': plugin,
    })


def render_glossarytext(plugin):
    return render_to_string('plugins/text.html', {
        'content': mark_safe(plugin.glossary_text)
    })


def render_html(plugin):
    return plugins.html.render_html(plugin)


def render_embed(plugin, **kwargs):
    return render_to_string('plugins/embed.html', {
        'json': oembed_json(plugin.url),
        'html': mark_safe(oembed_html(plugin.url)),
    })


def render_image(plugin, **kwargs):
    return render_to_string('plugins/image.html', {
        'plugin': plugin,
    })

def render_block(plugin, **kwargs):
    return plugin.render_html()


def register_renderers(renderer, models):
    renderer.register_string_renderer(
        models.RichText,
        render_richtext
    )

    renderer.register_string_renderer(
        models.HTML,
        render_html
    )

    renderer.register_string_renderer(
        models.External,
        render_embed
    )

    renderer.register_string_renderer(
        models.Image,
        render_image,
    )

    renderer.register_string_renderer(
        models.EventPlugin,
        events_plugins.render_events
    )

    renderer.register_string_renderer(
        models.ArticlePlugin,
        article_plugins.render_articles
    )

    renderer.register_string_renderer(
        models.Button,
        render_block
    )

renderer = TemplatePluginRenderer()
register_renderers(renderer, pages)
