# Generated by Django 5.0.6 on 2024-07-08 18:54

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='date_posted',
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
    ]
