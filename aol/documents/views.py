from django.utils.text import slugify
from django.views.generic import DetailView

from django_sendfile import sendfile

from aol.documents.models import Document


class DocumentDownloadView(DetailView):
    """
    TBD
    """
    queryset = Document.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        lake_counties = self.object.lake.county_set.values_list('name', flat=True)

        response = sendfile(request, self.object.file.path)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            '+'.join([
                '{}[{}]'.format(
                    slugify(str(self.object.lake)),
                    ','.join([slugify(c) for c in lake_counties])
                ),
                slugify(self.object.name)
            ])
        )

        return response
