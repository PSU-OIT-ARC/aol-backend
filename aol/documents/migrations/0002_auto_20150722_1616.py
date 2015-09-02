# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='friendly_filename',
            field=models.CharField(blank=True, help_text="\n        When this document is downloaded, this will be the filename (if blank, it will default to the document's original filename)\n    ", max_length=255),
            preserve_default=True,
        ),
    ]
