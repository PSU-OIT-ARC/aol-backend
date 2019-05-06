from django.contrib import admin


class MusselObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'agency', 'specie', 'date_checked', 'approved')
    list_filter = ('agency', 'specie')
    date_hierarchy = 'date_checked'

    raw_id_fields = ('lake', 'agency', 'specie')
