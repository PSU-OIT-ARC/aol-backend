from django.contrib import admin

from aol.resources import models


RESOURCE_FIELDSETS = (
    (None, {
        'fields': ('name', 'url', 'rank')
    }),
    ('Indexing', {
        'fields': ('lake', )
    })
)

class ResourceInline(admin.TabularInline):
    model = models.Resource
    fieldsets = RESOURCE_FIELDSETS
    extra = 0


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('lake', 'name', 'url', 'rank')
    list_display_links = ('name', )

    raw_id_fields = ('lake', )
    search_fields = ('name',
                     'lake__title', 'lake__reachcode')

    fieldsets = RESOURCE_FIELDSETS
