# Generated by Django 3.0.7 on 2021-01-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200918_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='active',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
