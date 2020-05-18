from django.utils.translation import gettext_lazy as _
from django.db import models
from django.template.loader import render_to_string
from content_editor.admin import ContentEditorInline

class ColorField(models.CharField):
    choices = (
        ('red', _("red")),
        ('orange', _("orange")),
        ('yellow', _("yellow")),
        ('olive', _("olive")),
        ('green', _("green")),
        ('teal', _("teal")),
        ('violett', _("violett")),
        ('purple', _("purple")),
        ('pink', _("pink")),
        ('brown', _("brown")),
        ('grey', _("grey")),
        ('black', _("black")),
    )

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['choices'] = self.choices
        kwargs['blank'] = True

        super().__init__(*args, **kwargs)

class AbstractBlock(models.Model):
    text = models.CharField(
        _("text"), max_length=240, blank=True,
    )

    color = ColorField()

    class Meta:
        abstract = True

    def render_html(self):
        raise NotImplementedError


class Button(AbstractBlock):

    style = models.CharField(_("style"), max_length=20, choices=(
        ('', _("none")),
        ('secondary', _("secondary"))
    ), default='', blank=True)

    align = models.CharField(
        _("alignment"), max_length=30, blank=True, choices=(
            ('', _("default")),
            ('center', _("center")),
            ('right', _("right")),
            ('block', _("block")),
        )
    )

    line_break = models.BooleanField(_("break"), default=True)

    target = models.CharField(_("target"), max_length=800)

    class Meta:
        abstract = True

    def render_html(self):
        return render_to_string(
            'button.html', {
                'button': self
            }
        )

    def __str__(self):
        return f'{self.text}'


class ButtonInline(ContentEditorInline):
    fieldsets = (
        (None, {
            'fields': (
                ('text', 'target'),
                'region', 'ordering',
            )
        }),
        (_("display"), {
            'classes': ('collapse',),
            'fields': ('color', 'style', 'line_break', 'align')
        })
    )
