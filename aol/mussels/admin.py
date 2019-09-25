import tempfile

from django.views.generic.edit import FormView
from django.core.management import call_command
from django.contrib import messages
from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django import http, forms


class MusselAdmin(admin.ModelAdmin):
    list_display = ('name', 'machine_name', 'is_scientific_name')
    list_filter = ('is_scientific_name',)


class LoadMusselObservationForm(forms.Form):
    datafile = forms.FileField()


class LoadMusselObservationView(FormView):
    template_name = 'admin/admin_action_intermediate_form.html'
    form_class = LoadMusselObservationForm

    def form_valid(self, form):
        try:
            datafile = tempfile.NamedTemporaryFile()
            for chunk in form.cleaned_data['datafile'].chunks():
                datafile.write(chunk)

            call_command('load_psmfc_mussel_observations', datafile.name)
            messages.success(self.request, "CSV has been loaded successfully")
        except Exception as exc:
            messages.error(self.request, "CSV was not loaded: {}".format(str(exc)))

        return http.HttpResponseRedirect(reverse('admin:mussels_musselobservation_changelist'))


class MusselObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'mussel', 'date_sampled',
                    'target', 'collecting_agency', 'collection_method')
    list_filter = ('mussel', 'collecting_agency', 'target', 'collection_method')
    date_hierarchy = 'date_sampled'

    search_fields = ('lake__title', 'lake__reachcode')
    raw_id_fields = ('lake', 'mussel')

    def get_urls(self):
        return [
            url(r'^load/$',
                self.admin_site.admin_view(LoadMusselObservationView.as_view()),
                {'current_app':self.admin_site.name},
                name='load-mussel-csv'
                )
        ] + super().get_urls()
