import os.path

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.conf import settings

from rest_framework import generics

from aol.documents.models import Document
from aol.photos.models import Photo

from . import models, serializers


class LakeListView(generics.ListAPIView):
    """
    TBD
    """
    serializer_class = serializers.LakeIndexSerializer

    def get_queryset(self):
        """
        TBD
        """
        status = self.request.query_params.get('status', 'major')
        if status == 'major':
            return models.Lake.active.major()
        return models.Lake.active.minor()

    # @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LakeDetailView(generics.RetrieveAPIView):
    """
    TBD
    """
    queryset = models.Lake.objects.all()
    serializer_class = serializers.LakeDetailSerializer

    # @method_decorator(cache_page(60 * 60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
