from django.contrib import admin

from aol.documents import models


DOCUMENT_FIELDSETS = (
    (None, {
        'fields': ('name', 'type', 'file', 'rank'),
    }),
    ('Indexing', {
        'fields': ('lake', )
    })
)

class DocumentInline(admin.TabularInline):
    model = models.Document
    fieldsets = DOCUMENT_FIELDSETS
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'lake', 'rank', 'uploaded_on')
    list_display_links = ('name', )
    list_filter = ('type', )

    date_hierarchy = 'uploaded_on'
    raw_id_fields = ('lake', )
    search_fields = ('name', 'lake__title', 'lake__reachcode')

    fieldsets = DOCUMENT_FIELDSETS
