import os.path

from django.db import models
from django.conf import settings


# this can't be a lambda because of Django migrations
def upload_to(instance, filename):
    return os.path.join('photos', filename)


class Photo(models.Model):
    """Stores all the photos attached to a lake"""
    THUMBNAIL_PREFIX = "thumbnail-"

    file = models.FileField(upload_to=upload_to, db_column="filename")
    taken_on = models.DateField(null=True, db_column="photo_date", blank=True)
    author = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    lake = models.ForeignKey('lakes.Lake', related_name='photos',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('lake', 'taken_on')

    def __str__(self):
        return '"{}" {} ({})'.format(self.caption, self.taken_on or 'N/A', self.file)

    # def exists(self):
    #     """Returns True if the file exists on the filesystem"""
    #     try:
    #         open(self.file.path)
    #     except IOError:
    #         return False
    #     return True

    # @property
    # def thumbnail_url(self):
    #     """Returns the complete path to the photo's thumbnail from MEDIA_URL"""
    #     return settings.MEDIA_URL + os.path.relpath(self._thumbnail_path, settings.MEDIA_ROOT)

    # @property
    # def _thumbnail_path(self):
    #     """Returns the abspath to the thumbnail file, and generates it if needed"""
    #     filename = self.THUMBNAIL_PREFIX + os.path.basename(self.file.name)
    #     path = os.path.join(os.path.dirname(self.file.path), filename)
    #     try:
    #         open(path).close()
    #     except IOError:
    #         self._generate_thumbnail(path)

    #     return path

    # def _generate_thumbnail(self, save_to_location):
    #     """Generates a thumbnail and saves to to the save_to_location"""
    #     SIZE = (400, 300)
    #     im = Image.open(self.file.path)
    #     im.thumbnail(SIZE, Image.ANTIALIAS)
    #     im.save(save_to_location)
