from django.contrib import admin

from aol.photos import models


PHOTO_FIELDSETS = (
    (None, {
        'fields': ('file', 'caption', 'author', 'taken_on'),
    }),
    ('Indexing', {
        'fields': ('lake', )
    })
)

class PhotoInline(admin.TabularInline):
    model = models.Photo
    fieldsets = PHOTO_FIELDSETS
    extra = 0


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('lake', 'caption', 'author', 'taken_on')
    list_display_links = ('caption', )

    date_hierarchy = 'taken_on'
    raw_id_fields = ('lake', )
    search_fields = ('author', 'caption',
                     'lake__title', 'lake__reachcode')

    fieldsets = PHOTO_FIELDSETS
