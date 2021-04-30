import os.path

from django.views.generic import View
from django.http import Http404
from django.conf import settings

from django_sendfile import sendfile
from rest_framework import generics

from aol.lakes.models import Lake
from aol.lakes.serializers import LakeDetailSerializer


class LakeListView(View):
    """
    TBD
    """
    def get(self, request, *args, **kwargs):
        """
        TBD
        """
        status = request.GET.get('status', None)
        render_format = kwargs.get('format', None)

        if status is None:
            raise Http404

        cached_name = 'lakes-{}.json'.format(status)
        path = os.path.join(settings.MEDIA_ROOT, cached_name)
        if not os.path.exists(path):
            raise Http404

        return sendfile(request, path, mimetype='application/json')


class LakeDetailView(generics.RetrieveAPIView):
    """
    TBD
    """
    queryset = Lake.objects.all()
    serializer_class = LakeDetailSerializer
