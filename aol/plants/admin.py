import tempfile

from django.views.generic.edit import FormView
from django.core.management import call_command
from django.contrib import messages
from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django import http, forms

from aol.plants import enums


class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'common_name', 'is_native', 'noxious_weed_designation')
    list_filter = ('is_native', 'noxious_weed_designation')
    search_fields = ('name', 'common_name')


REPORTING_SOURCE_CHOICES = (
    ('CLR', enums.REPORTING_SOURCE_CLR),
    ('IMAP', enums.REPORTING_SOURCE_IMAP)
)

class LoadPlantObservationForm(forms.Form):
    source = forms.ChoiceField(choices=REPORTING_SOURCE_CHOICES)
    datafile = forms.FileField()


class LoadPlantObservationView(FormView):
    template_name = 'admin/admin_action_intermediate_form.html'
    form_class = LoadPlantObservationForm

    def form_valid(self, form):
        try:
            datafile = tempfile.NamedTemporaryFile()
            for chunk in form.cleaned_data['datafile'].chunks():
                datafile.write(chunk)

            source = form.cleaned_data['source']
            if source == enums.REPORTING_SOURCE_CLR:
                call_command('load_clr_plant_observations', datafile.name)
            elif source == enums.REPORTING_SOURCE_IMAP:
                call_command('load_imap_plant_observations', datafile.name)
            messages.success(self.request, "CSV has been loaded successfully")
        except Exception as exc:
            messages.error(self.request, "CSV was not loaded: {}".format(str(exc)))

        return http.HttpResponseRedirect(reverse('admin:plants_plantobservation_changelist'))


class PlantObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'plant', 'observation_date', 'source', 'survey_org')
    list_filter = ('source',)
    date_hierarchy = 'observation_date'

    search_fields = ('lake__title', 'lake__reachcode')
    raw_id_fields = ('lake', 'plant')

    def get_urls(self):
        return [
            url(r'^load/$',
                self.admin_site.admin_view(LoadPlantObservationView.as_view()),
                {'current_app':self.admin_site.name},
                name='load-plant-csv'
                )
        ] + super().get_urls()
