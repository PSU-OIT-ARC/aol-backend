from django.contrib import admin


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'lake', 'rank', 'uploaded_on')
    list_display_links = ('name', )
    list_filter = ('type', )

    date_hierarchy = 'uploaded_on'
    raw_id_fields = ('lake', )
    search_fields = ('name', 'lake__title')

    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'file', 'rank'),
        }),
        ('Indexing', {
            'fields': ('lake', )
        })
    )
