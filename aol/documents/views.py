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

        return sendfile(request, self.object.file.path)
