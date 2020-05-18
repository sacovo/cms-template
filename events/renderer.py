from feincms3.renderer import TemplatePluginRenderer
from cms.renderer import register_renderers

from events import models

renderer = TemplatePluginRenderer()

register_renderers(renderer, models)
