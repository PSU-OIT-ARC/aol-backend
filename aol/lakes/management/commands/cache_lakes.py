import os.path
import json
import io

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from aol.lakes.serializers import LakeIndexSerializer
from aol.lakes.models import Lake


class Command(BaseCommand):
    help = "Caches lake index data"

    def generate_cache(self, serializer, path):
        data = io.StringIO()
        data.write(json.dumps(serializer.data, separators=(',', ':')))
        data.seek(0)

        with open(path, 'w') as f:
            f.write(data.read())

    def handle(self, *args, **options):
        serializer = LakeIndexSerializer(Lake.active.major(), many=True)
        path = os.path.join(settings.MEDIA_ROOT, 'lakes-major.json')
        self.generate_cache(serializer, path)

        serializer = LakeIndexSerializer(Lake.active.minor(), many=True)
        path = os.path.join(settings.MEDIA_ROOT, 'lakes-minor.json')
        self.generate_cache(serializer, path)
