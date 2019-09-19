# Generated by Django 2.2.2 on 2019-09-04 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='is_native',
            field=models.NullBooleanField(choices=[(True, 'Native'), (False, 'Non-native'), (None, '')], default=None),
        ),
    ]
