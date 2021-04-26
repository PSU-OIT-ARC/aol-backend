from django.views.generic import DetailView

from django_sendfile import sendfile

from aol.photos.models import Photo


class PhotoAccessView(DetailView):
    """
    TBD
    """
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return sendfile(request, self.object.file.path)
