from django.db import models


class Resource(models.Model):
    """
    TBD
    """
    name = models.CharField(max_length=255)
    url = models.URLField()

    rank = models.IntegerField(verbose_name="Weight",
                               help_text="Defines the order in which items are listed.")
    lake = models.ForeignKey('lakes.Lake', related_name='resources',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('lake', 'rank')

    def __str__(self):
        return '{} ({})'.format(self.name, self.lake)
