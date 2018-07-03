# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180629_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
            preserve_default=True,
        ),
    ]
