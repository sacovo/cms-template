from content_editor.admin import ContentEditorInline
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from feincms3_sites.middleware import current_site


class EventPlugin(models.Model):
    events = models.ManyToManyField(
        "events.Event", related_name="+",
        verbose_name=_("events"), blank=True,
        related_query_name='+',
    )

    title = models.CharField(_("title"), blank=True, max_length=180)
    count = models.IntegerField(_("count"), default=3)

    template_key = models.CharField(
        max_length=100, default='events/plugins/default.html',
        choices=settings.EVENT_TEMPLATE_CHOICES,
    )

    def __str__(self):
        return self.title or _("events")

    class Meta:
        abstract = True
        verbose_name = _("event plugin")
        verbose_name_plural = _("event plugins")


class EventPluginInline(ContentEditorInline):
    autocomplete_fields = [
        'events',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'events',
                'title',
                'count',
                'ordering',
                'region'
            )
        }),
        (_("advanced"), {
            'classes': ('collapse',),
            'fields': (
                'template_key',
            )
        }),
    )


def get_event_list(plugin):
    if plugin.events.exists():
        return plugin.events.all()
    from events.models import Event

    events = Event.objects.filter(
        language_code=plugin.parent.language_code,
        end_date__gte=timezone.now()
    )

    return events[:plugin.count]


def render_events(plugin, **kwargs):
    return render_to_string(
        plugin.template_key, {
            'events': get_event_list(plugin),
            'plugin': plugin,
        }
    )
