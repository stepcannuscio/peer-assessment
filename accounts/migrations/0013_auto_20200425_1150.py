# Generated by Django 3.0.5 on 2020-04-25 16:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200425_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peer_assessment',
            name='end_date',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='peer_assessment',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 25, 11, 50, 26, 802083)),
        ),
    ]
