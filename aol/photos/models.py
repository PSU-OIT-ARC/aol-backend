import os.path

from django.urls import reverse
from django.db import models


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

    def get_absolute_url(self):
        return reverse('api:photo-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '"{}" {} ({})'.format(self.caption, self.taken_on or 'N/A', self.file)
