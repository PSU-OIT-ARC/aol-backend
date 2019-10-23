import requests

from django.contrib.flatpages.models import FlatPage
from django.conf import settings

from emcee.backends.aws.processors import ssm
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from aol.documents.models import Document
from aol.photos.models import Photo

from . import serializers


class ArcGISAuthTokenView(APIView):
    """
    TBD
    """
    def get(self, request, format=None):
        if settings.DEBUG:
            return Response({})

        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'accept': 'application/json',
                   'cache-control': 'no-cache'}
        ssm_params = {'region': settings.AWS_REGION,
                      'ssm_prefix': settings.SSM_KEY}
        payload = {'client_id': ssm('ArcGISClientID', **ssm_params),
                   'client_secret': ssm('ArcGISClientSecret', **ssm_params),
                   'grant_type': 'client_credentials'}
        response = requests.post(settings.ARCGIS_ONLINE_TOKEN_URL,
                                 data=payload,
                                 headers=headers)
        return Response(response.json())


class FlatPageListView(generics.ListAPIView):
    """
    TBD
    """
    queryset = FlatPage.objects.all()
    serializer_class = serializers.FlatPageSerializer


class FlatPageDetailView(generics.RetrieveAPIView):
    """
    TBD
    """
    queryset = FlatPage.objects.all()
    serializer_class = serializers.FlatPageSerializer
    lookup_field = 'url'
    lookup_url_kwarg = 'slug'

    def get_object(self):
        if self.lookup_url_kwarg in self.kwargs:
            self.kwargs[self.lookup_url_kwarg] = '/{}/'.format(self.kwargs[self.lookup_url_kwarg])

        return super().get_object()
