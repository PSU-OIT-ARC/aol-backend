from django.contrib import admin


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('lake', 'caption', 'author', 'taken_on')
    list_display_links = ('caption', )

    date_hierarchy = 'taken_on'
    raw_id_fields = ('lake', )
    search_fields = ('author', 'caption', 'lake__title')

    fieldsets = (
        (None, {
            'fields': ('file', 'caption', 'author', 'taken_on'),
        }),
        ('Indexing', {
            'fields': ('lake', )
        })
    )
