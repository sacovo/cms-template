from admin_ordering.admin import OrderableAdmin
from django.contrib import admin

from link_collections.models import Link, Collection
# Register your models here.


class LinkInline(OrderableAdmin, admin.TabularInline):
    model = Link
    ordering_field = 'order'
    ordering_field_hide_input = True

    fields = ('text', 'target', 'color', 'order')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name']

    inlines = [
        LinkInline
    ]

    search_fields = ['name']
