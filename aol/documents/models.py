import os.path

from django.urls import reverse
from django.db import models

from aol.documents import enums


# this can't be lambda because of Django migrations
def upload_to(instance, filename):
    return os.path.join('pages', filename)


class Document(models.Model):
    """
    Stores all the documents attached to a lake like PDFs, and whatever else an
    admin wants to upload (except Photos which are handled in their own model)
    """
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to)
    rank = models.IntegerField(verbose_name="Weight",
                               help_text="Defines the order in which items are listed.")
    uploaded_on = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=enums.DOCUMENT_TYPE_CHOICES)
    friendly_filename = models.CharField(max_length=255, blank=True,
                                         help_text="Filename when document is downloaded.")

    lake = models.ForeignKey('lakes.Lake', related_name='documents',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('lake', 'rank')

    def get_absolute_url(self):
        return reverse('api:doc-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} ({})'.format(self.name, self.lake)
