# Generated by Django 3.0.7 on 2020-08-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_main_set_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='link',
            field=models.TextField(blank=True, default='-', null=True),
        ),
        migrations.AddField(
            model_name='main',
            name='tell',
            field=models.TextField(blank=True, default='-', null=True),
        ),
    ]
