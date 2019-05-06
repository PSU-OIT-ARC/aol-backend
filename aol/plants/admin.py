from django.contrib import admin


class PlantObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'plant', 'observation_date', 'source', 'survey_org')
    list_filter = ('source',)
    date_hierarchy = 'observation_date'

    raw_id_fields = ('lake', 'plant')
