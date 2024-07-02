# Generated by Django 5.0.6 on 2024-07-01 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0014_delete_historicaluser'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, to='auth.permission'),
        ),
    ]
