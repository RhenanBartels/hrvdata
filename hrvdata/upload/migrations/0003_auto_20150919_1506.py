# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='start_signal',
            field=models.FloatField(default=0.0),
        ),
    ]
