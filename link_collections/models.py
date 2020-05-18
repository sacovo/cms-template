from django.db import models
from django.utils.translation import gettext_lazy as _
from cms.plugins import ColorField
# Create your models here.


class Collection(models.Model):
    name = models.CharField(_("name"), max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")
        ordering = ['name']


class Link(models.Model):
    collection = models.ForeignKey(
        Collection, models.CASCADE,
        verbose_name=_("Collection")
    )

    text = models.CharField(_("text"), max_length=120)
    target = models.URLField(_("target"))

    color = ColorField()

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        ordering = ['order']
