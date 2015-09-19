# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('signal', models.OneToOneField(primary_key=True, serialize=False, to='upload.Tachogram')),
                ('start_signal', models.FloatField()),
                ('end_signal', models.FloatField()),
                ('tv_segment_size', models.IntegerField(default=30)),
                ('tv_overlap_size', models.IntegerField(default=0)),
                ('sp_sampling_freq', models.IntegerField(default=4)),
                ('sp_window_func', models.IntegerField(default=0)),
                ('sp_detrending', models.IntegerField(default=0)),
                ('sp_segment_size', models.IntegerField(default=256)),
                ('sp_overlap_size', models.IntegerField(default=128)),
                ('sp_model_order', models.IntegerField(default=16)),
                ('tf_sampling_freq', models.IntegerField(default=5)),
                ('tf_window_func', models.IntegerField(default=0)),
                ('tf_detrending', models.IntegerField(default=0)),
                ('tf_segment_size', models.IntegerField(default=512)),
                ('tf_overlap_size', models.IntegerField(default=256)),
                ('tf_model_order', models.IntegerField(default=16)),
            ],
        ),
    ]
